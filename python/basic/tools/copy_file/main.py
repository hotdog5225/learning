import os
old_file_path = "log1.log"
new_file_path = "log2.log"

if __name__ == '__main__':
    pos_old = 0
    with open(new_file_path, "a") as f_new:
        # 读取旧的log
        with open(old_file_path, "r") as f_old:
            old_size = os.path.getsize(old_file_path)
            f_old.seek(pos_old, 0)
            while True:
                # 判断是否重启
                new_size = os.path.getsize(old_file_path)
                if new_size < old_size:
                    print("rebooted")
                    f_old.seek(0, 0)

                old_size = new_size

                line = f_old.readline().strip()
                pos_old = f_old.tell()
                f_old.seek(pos_old, 0)

                if line:
                    print("line is {}".format(line))
                    # # 写入新的日志
                    f_new.write(line + '\n')
                    f_new.flush()



