import pandas as pd
import os
import time

from main_analyzer import main_analyzer
from utils.Git import Git
from utils.file_manager import FileManager

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
def main():
    repo_target_path_root = ROOT_DIR+"/data/clones"
    df_topic = pd.read_csv(ROOT_DIR + '/inputs.csv')
    config = df_topic.config.values.tolist()
    config_only = df_topic.config_only.values.tolist()
    repo_name_list = df_topic.repo_name.values.tolist()

    if not os.path.exists(ROOT_DIR+'/data'):
        os.makedirs(ROOT_DIR+'/data')
    if not os.path.exists(ROOT_DIR+'/data/logs'):
        os.makedirs(ROOT_DIR+'/data/logs')
    if not os.path.exists(ROOT_DIR+'/data/clones'):
        os.makedirs(ROOT_DIR+'/data/clones')
    if not os.path.exists(ROOT_DIR+'/data/csv'):
        os.makedirs(ROOT_DIR+'/data/csv')
    config_list = []
    for index_ in range(len(repo_name_list)):
        if 'from' in config[index_] or 'import' in config[index_]:
            if not config_only[index_] in config_list:
                config_list.append(config_only[index_])
    #print (config_list)
    for index_2 in range(131,len(repo_name_list)):
        #if not file_name[index] is np.nan:
        repo_proj = repo_name_list[index_2]
        print(index_2, repo_proj, config[index_2])

        if 'from' in config[index_2] or 'import' in config[index_2]:
            #if '/' in repo_proj:

            repository_url = "https://github.com/" + repo_proj + ".git"
            #print (repository_url)
            repo_name = repo_proj.split('/')[1]
            log_tags_path = ROOT_DIR+'/data/logs/tags_' + repo_name+'_'+str(index_2)+ '.txt'
            repo_root = ROOT_DIR+'/data/clones/'+repo_name
            if not os.path.exists(repo_root):
                code = Git.clone_git_repository(url=repository_url, target_path=repo_target_path_root)
            else:
                code = 0
            if code == 0:
                Git.git_fetch_tags(repo_root)
                logs = Git.git_fetch_tags_sorts(repo_root, log_tags_path)
                tag_list = []
                tag_date_list = []

                for line in logs.split('\n'):
                    if len(line) > 0:
                        split_line = line.strip().split(' ')
                        tag = split_line[0]
                        tag = tag.replace('refs/tags/', '')
                        date = split_line[1]+' '+split_line[2]+ ' '+split_line[3]+' ' +split_line[4]+ ' '+split_line[5]
                        #print (tag, date)
                        tag_list.append(tag)
                        tag_date_list.append(date)
                print ('  ----total tags found: ', len(tag_list))
                if len(tag_list) > 0:
                    with open(log_tags_path, "w") as text_file:
                        text_file.write(logs)
                    for tag_id in range((len(tag_list))):
                        tag = tag_list[tag_id]
                        print ('     ---- now analysing: ', tag_id, tag)
                        Git.git_checkout(repo_root, tag)
                        os.chdir(ROOT_DIR)
                        main_analyzer(repo_root, repo_proj, tag, automl_configs=config_list, save_json=True)
                else:
                    os.chdir(ROOT_DIR)
                    main_analyzer(repo_root, repo_proj, 'latest', automl_configs=config_list, save_json=True)
                # Remove the clone project after completing analysis
                FileManager.remove_clone(repo_root)
            time.sleep(5)
            #os.rename(repo_path, repo_path2)
if __name__ == '__main__':
    main()