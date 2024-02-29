import os
import difflib
import datetime


class ConfigManager:
    def __init__(self, root_dir="ConfigBack"):
        self.root = root_dir
        if not os.path.exists(self.root):
            os.mkdir(self.root)
        self.diff_threshold = 0.6
        self.report = None

    def diff_report(self, old, new):
        diff_info = difflib.ndiff(old.split('\n'), new.split('\n'))
        self.report = '\n'.join(diff_info)

    def diff_check(self, old, new):
        matcher = difflib.SequenceMatcher(None, old, new)
        similarity_ratio = matcher.ratio()
        return similarity_ratio < self.diff_threshold

    def save_config(self, back_path, ip, new):
        file_name = ip + str(datetime.datetime.now()).split()[1].split('.')[0].replace(':', '_') + '.txt'
        file_path = os.path.join(back_path, file_name)
        with open(file_path, 'w') as f:
            f.write(new)

    def backup(self, ip_net, config_new):
        ip = ip_net.replace('.', '_')
        newest_file = None
        newest_time = 0
        today = str(datetime.datetime.now()).split()[0].replace('-', '_')
        back_path = os.path.join(self.root, today)
        if not os.path.exists(back_path):
            os.mkdir(back_path)
        check_list = [file_name for file_name in os.listdir(back_path) if file_name.startswith(ip)]
        if check_list:
            for file_name in check_list:
                file_path = os.path.join(back_path, file_name)
                ctime = os.path.getctime(file_path)
                if ctime > newest_time:
                    newest_time = ctime
                    newest_file = file_path
            with open(newest_file) as f:
                config_old = f.read()
            if self.diff_check(config_old, config_new):
                self.diff_report(config_old, config_new)
                self.save_config(back_path, ip, config_new)
        else:
            self.save_config(back_path, ip, config_new)

