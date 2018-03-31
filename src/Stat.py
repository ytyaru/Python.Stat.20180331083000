import os, os.path, pathlib, shutil, stat
import functools

class Stat:
    @classmethod
    def GetSize(cls, path):
        if os.path.isfile(path): return os.path.getsize(path)
        elif os.path.isdir(path):
            if hasattr(os, 'scandir'): cls.GetDirectorySize_ByScanDir(path) # Python 3.5
            elif hasattr(os,'listdir'): cls.GetDirectorySize_ByListDir(path)
            else: raise Exception('ディレクトリのサイズを計測するメソッドが見つかりません。')
            
    # https://code.i-harness.com/ja/q/153f1d
    @classmethod
    def GetDirectorySize_ByListDir(cls, path):
        prepend = functools.partial(os.path.join, p)
        return sum([(os.path.getsize(f) if os.path.isfile(f) and not os.path.islink(f) else getFolderSize(f)) for f in map(prepend, os.listdir(p))])

    @classmethod
    def GetDirectorySize_ByScanDir(cls, path):
        with os.scandir(path) as scand:
            return sum([s.stat(follow_symlinks=False).st_size for s in scand if s.is_file(follow_symlinks=False)]) + \
            + sum([getTotFldrSize(s.path) for s in scand if s.is_dir(follow_symlinks=False)])

    @classmethod
    def DiskUsage(cls, path): return shutil.disk_usage(path)

    @classmethod
    def SetMode(cls, path, mode=0o755):
        # 3桁の8進数値
        if type(mode) == int:
            pathlib.Path(path).chmod(mode)
        # -rwxrwxrwx のような文字列
        elif type(mode) == str:
            cls.__SetModeFromName(path, mode)
    @classmethod
    def GetMode(cls, path): return oct(os.stat(path).st_mode)
    @classmethod
    def GetModeName(cls, path): return stat.filemode(os.stat(path).st_mode)
    # -rwxrwxrwx
    @classmethod
    def __SetModeFromName(cls, path, mode_name):
        mname = mode_name.strip()
        if mname.startswith('-'): mname = mname[1:]
        mode_names = [
            '---',
            '--x',
            '-w-',
            '-wx',
            'r--',
            'r-x',
            'rw-',
            'rwx'
        ]
        try:
            owner = [i for i, n in enumerate(mode_names) if n == mname[0:3]][0]
            group = [i for i, n in enumerate(mode_names) if n == mname[3:6]][0]
            other = [i for i, n in enumerate(mode_names) if n == mname[6:9]][0]
            cls.SetMode(path, int('0{}{}{}'.format(owner, group, other), base=8))
            #cls.SetMode(path, int('0o{}{}{}'.format(owner, group, other)))
            #return oct(str(owner)+str(group)+str(other))
        except:
            import traceback
            traceback.print_exc()
            raise Exception('引数mode_nameが不正値です。{}。\'-rwxrwxrwx\'の書式で入力してください。owner, group, other, の順に次のパターンのいずれかを指定します。pattern={}。r,w,xはそれぞれ、読込、書込、実行の権限です。-は権限なしを意味します。'.format(mode_name, mode_names))

    # epock
    @classmethod
    def GetModifiedDateTime(cls, path):
        return os.stat(path).st_mtime
        #return os.path.getmtime(path)

    @classmethod
    def SetModifiedDateTime(cls, path, mtime):
        os.utime(path, (os.stat(path).st_atime, mtime))

    @classmethod
    def GetAccessedDateTime(cls, path):
        return os.stat(path).st_atime
        #return os.path.getatime(path)
    @classmethod
    def SetAccessedDateTime(cls, path, atime):
        os.utime(path, (atime, os.stat(path).st_mtime))

    @classmethod
    def GetChangedMetaDataDateTime(cls, path):
        return os.stat(path).st_ctime
        #return os.path.getctime(path)
    @classmethod
    def GetCreatedDateTime(cls, path):
        s = os.stat(path)
        if hasattr(s, 'st_birthtime'): return s.st_birthtime
        else: return s.st_ctime
        
    @classmethod
    def GetOwnUserId(cls, path): return os.stat(path).st_uid
    @classmethod
    def GetOwnGroupId(cls, path): return os.stat(path).st_gid
    @classmethod
    def GetHardLinkNum(cls, path): return os.stat(path).st_nlink
    @classmethod
    def GetINode(cls, path): return os.stat(path).st_ino
    @classmethod
    def GetDeviceId(cls, path): return os.stat(path).st_dev

