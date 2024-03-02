import os
import difflib
import datetime


class ConfigManager:
    def __init__(self, root_dir="ConfigBack"):
        self.root = root_dir
        self._check_dir(self.root)
        self.diff_threshold = 0.7
        self.report = None

    def diff_report(self, old, new):
        diff_info = difflib.ndiff(old.split('\n'), new.split('\n'))
        self.report = "\n".join(diff_info)

    def diff_check(self, old, new):
        # True: 配置不变
        # False: 配置变化
        matcher = difflib.SequenceMatcher(None, old.split('\n'), new.split('\n'))
        similarity_ratio = matcher.ratio()
        print(similarity_ratio)
        return similarity_ratio > self.diff_threshold

    def save_config(self, back_path, ip, new_config):
        file_name = ip + str(datetime.datetime.now()).split()[1].split('.')[0].replace(':', '_') + '.txt'
        file_path = os.path.join(back_path, file_name)
        with open(file_path, 'w') as f:
            f.write(new_config)

    def _check_dir(self, path):
        if not os.path.exists(path):
            os.mkdir(path)

    def backup(self, ip_net, config_new):
        ip = ip_net.replace('.', '_')
        newest_file = None
        newest_time = 0
        today = str(datetime.datetime.now()).split()[0].replace('-', '_')
        back_path = os.path.join(self.root, today)
        self._check_dir(back_path)

        # 在当天目录下找出跟当前IP一样的历史备份文件
        check_list = [file_name for file_name in os.listdir(back_path) if file_name.startswith(ip)]
        if check_list:
            # 找出最新的历史文件
            for file_name in check_list:
                file_path = os.path.join(back_path, file_name)
                ctime = os.path.getctime(file_path)
                if ctime > newest_time:
                    newest_time =ctime
                    newest_file = file_path

            with open(newest_file) as f:
                config_old = f.read()
            if not self.diff_check(config_old, config_new):
                self.diff_report(config_old, config_new)
                self.save_config(back_path, ip, config_new)
        else:
            self.save_config(back_path, ip, config_new)