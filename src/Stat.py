import os, os.path, pathlib, shutil, stat
import functools
import time, datetime

class Stat:
    def __init__(self, path):
        self.__path = path
        if not os.path.exists(str(self.__path)): raise ValueError('引数pathには存在するファイルかディレクトリを指定してください。')
        self.__stat = os.stat(self.__path)
    @property
    def Stat(self): return self.__stat
    @property
    def Path(self): return self.__path
    @property
    def Size(self): return self.GetSize(self.Path)

    @property
    def Mode(self): return self.GetMode(self.Path)
    @Mode.setter
    def Mode(self, v): self.SetMode(self.Path, v)
    @property
    def ModeName(self): return self.GetModeName(self.Path)

    @property
    def Modified(self): return self.GetModified(self.Path)
    @Modified.setter
    def Modified(self, v): self.SetModified(self.Path, v)

    @property
    def Accessed(self): return self.GetAccessed(self.Path)
    @Accessed.setter
    def Accessed(self, v): self.SetAccessed(self.Path, v)

    @property
    def Created(self): return self.GetCreated(self.Path)
    @property
    def ChangedMeta(self): return self.GetChangedMeta(self.Path)

    @property
    def OwnUserId(self): return self.GetOwnUserId(self.Path)
    @property
    def OwnGroupId(self): return self.GetOwnGroupId(self.Path)
    @property
    def HardLinkNum(self): return self.GetHardLinkNum(self.Path)
    @property
    def INode(self): return self.GetINode(self.Path)
    @property
    def DeviceId(self): return self.GetDeviceId(self.Path)

    @classmethod
    def GetSize(cls, path):
        if os.path.isfile(path): return os.path.getsize(path)
        elif os.path.isdir(path):
            if hasattr(os, 'scandir'): return cls.GetDirectorySize_ByScanDir(path) # Python 3.5
            elif hasattr(os,'listdir'): return cls.GetDirectorySize_ByListDir(path)
            else: raise Exception('ディレクトリのサイズを計測するメソッドが見つかりません。')
            
    # https://code.i-harness.com/ja/q/153f1d
    @classmethod
    def GetDirectorySize_ByListDir(cls, path):
        prepend = functools.partial(os.path.join, path)
        return sum([(os.path.getsize(f) if os.path.isfile(f) and not os.path.islink(f) else cls.GetDirectorySize_ByListDir(f)) for f in map(prepend, os.listdir(path))])

    @classmethod
    def GetDirectorySize_ByScanDir(cls, path):
        return sum([s.stat(follow_symlinks=False).st_size for s in os.scandir(path) if s.is_file(follow_symlinks=False)]) + \
        + sum([cls.GetDirectorySize_ByScanDir(s.path) for s in os.scandir(path) if s.is_dir(follow_symlinks=False)])

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
    def GetMode(cls, path): return os.stat(path).st_mode
    @classmethod
    def GetModeName(cls, path): return stat.filemode(os.stat(path).st_mode)
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
        except:
            raise ValueError('引数mode_nameが不正値です。\'{}\'。\'-rwxrwxrwx\'の書式で入力してください。owner, group, other, の順に次のパターンのいずれかを指定します。pattern={}。r,w,xはそれぞれ、読込、書込、実行の権限です。-は権限なしを意味します。'.format(mode_name, mode_names))

    # epock
    @classmethod
    def GetModified(cls, path):
        return cls.__GetTimeFromEpoch(os.stat(path).st_mtime)
    @classmethod
    def SetModified(cls, path, mtime):
        os.utime(path, (os.stat(path).st_atime, cls.__ToEpoch(mtime)))

    @classmethod
    def GetAccessed(cls, path):
        return cls.__GetTimeFromEpoch(os.stat(path).st_atime)
    @classmethod
    def SetAccessed(cls, path, atime):
        os.utime(path, (cls.__ToEpoch(atime), os.stat(path).st_mtime))

    @classmethod
    def GetChangedMeta(cls, path):
        return cls.__GetTimeFromEpoch(os.stat(path).st_ctime)
    @classmethod
    def GetCreated(cls, path):
        s = os.stat(path)
        if hasattr(s, 'st_birthtime'): return cls.__GetTimeFromEpoch(s.st_birthtime)
        else: return cls.__GetTimeFromEpoch(s.st_ctime)

    @classmethod
    def __GetTimeFromEpoch(cls, epoch):
        return epoch, datetime.datetime(*time.localtime(epoch)[:6])
 
    @classmethod
    def __ToEpoch(cls, value):
        if type(value) == int: return value
        if type(value) == float: return value
        elif type(value) == time: return value.localtime()
        elif type(value) == datetime.datetime: return int(time.mktime(value.timetuple()))
        elif type(value) == str:
            return int(time.mktime(cls.__StrToDateTime(value).timetuple()))
        else: raise TypeError('引数mtimeはint型のエポックタイム値、time型、datetime型, strkk型のいずれかにしてください。')

    @classmethod
    def __StrTo(cls, value):
        formats = ['%Y-%m-%d %H:%M:%S',
                   '%Y/%m/%d %H:%M:%S',
                   '%Y/%m/%d %H:%M:%S%z',# +0900
                   '%Y-%m-%d %H:%M:%S%z'
        ]
        for f in formats:
            try: return datetime.datetime.strptime(value)
            except: continue
        raise ValueError('引数値\'{}\'は日付に変換できませんでした。次の書式のいずれかにしてください。formats={}'.format(formats))

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

