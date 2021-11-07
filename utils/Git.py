import os
import subprocess
from datetime import date
class Git:

    @staticmethod
    def git_fetch_tags(target_path):
        os.chdir(target_path)
        git_command = "git fetch --all --tags"
        p = subprocess.Popen(git_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output = ""
        for line in p.stdout.readlines():
            output = output + str(line) + '\n'
        retval = p.wait()
        return retval

    @staticmethod
    def git_fetch_tags_sorts(target_path, log_path):
        os.chdir(target_path)
        print (target_path)
        git_command = "git for-each-ref --sort=creatordate --format '%(refname) %(creatordate)' refs/tags"
        p = subprocess.Popen(git_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output = ""
        for line in p.stdout.readlines():
            output = output + str(line) + '\n'
        retval = p.wait()
        return output

    @staticmethod
    def git_checkout(target_path, tag):
        os.chdir(target_path)
        git_command = "git checkout "+str(tag)
        subprocess.Popen(git_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    @staticmethod
    def clone_git_repository(url, target_path):
        os.chdir(target_path)
        git_clone_command = "git clone " + url
        print("git clone {} ...".format(url))
        p = subprocess.Popen(git_clone_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output = ""
        for line in p.stdout.readlines():
            output = output + str(line) + '\n'
        retval = p.wait()
        if retval == 0:
            print(" Repository cloned successfully!")
        else:
            print(" Error in cloning!")
            print(output)
        return retval

    @staticmethod
    def extract_git_commit_logs(repo_path, log_path):
        os.chdir(repo_path)
        git_log_command = "git --no-pager log --pretty=format:\"%H|%ad|%an|%s\" --date=short >" + log_path
        # print(git_log_command)
        print("Extracting commit logs from repository in :{}".format(repo_path))
        p = subprocess.Popen(git_log_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output = ""
        for line in p.stdout.readlines():
            output = output + str(line) + '\n'
        retval = p.wait()
        if retval == 0:
            print("Commit log extracted successfully!")
        else:
            print("Error in commit log extraction!")
            print(output)
        return retval

    @staticmethod
    def list_git_commits(log_path):
        commit_list = []
        try:
            with open(log_path, "r", encoding='utf-8') as fp:
                text_lines = fp.readlines()
                for line in text_lines:
                    try:
                        log_parts = line.split('|')
                        # print(log_parts)
                        csha = log_parts[0]
                        c_date = log_parts[1]
                        commit_list.append([csha, c_date])
                    except:
                        pass
            fp.close()
            no_commit = len(commit_list)
            commit_list1 = []
            for i in range(no_commit - 1, -1, -1):
                commit_list1.append(commit_list[i])
        except:
            print("Error in file reading")
        return commit_list1

    @staticmethod
    def get_date_days_diff(date1, date2):
        dy1, dm1, dd1 = date1.split('-')
        dy2, dm2, dd2 = date2.split('-')

        d1 = date(int(dy1), int(dm1), int(dd1))
        d2 = date(int(dy2), int(dm2), int(dd2))

        delta = d2 - d1
        no_days = delta.days
        # print(delta.days)
        return no_days