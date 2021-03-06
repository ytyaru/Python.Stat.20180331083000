import sys, os, os.path, pathlib
print(pathlib.Path(__file__).parent.parent / 'src')
sys.path.append(str(pathlib.Path(__file__).parent.parent / 'src'))
from Stat import Stat

def MakeDummy(path, size):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'wb') as f:
        f.write(b'\0'*size)

if __name__ == '__main__':
    target_root = '/tmp/work/__TEST__'
    target_dummy = os.path.join(target_root, 'a.dummy')
    MakeDummy(target_dummy, 1024)
    assert(1024 == Stat.GetSize(target_dummy))
    print(Stat.DiskUsage(target_root))

    mode = Stat.GetMode(target_dummy)
    print(mode)
    Stat.SetMode(target_dummy, 0o755)
    print(Stat.GetMode(target_dummy))
    print(Stat.GetModeName(target_dummy))
    Stat.SetMode(target_dummy, Stat.GetModeName(target_dummy))
    print(Stat.GetMode(target_dummy))
    Stat.SetMode(target_dummy, '-rwxrw-r--')
    print(Stat.GetMode(target_dummy))

    print(Stat.GetModifiedDateTime(target_dummy))
    print(Stat.GetCreatedDateTime(target_dummy))
    print(Stat.GetChangedMetaDataDateTime(target_dummy))
    print(Stat.GetAccessedDateTime(target_dummy))

    print(Stat.GetOwnUserId(target_dummy))
    print(Stat.GetOwnGroupId(target_dummy))
    print(Stat.GetHardLinkNum(target_dummy))
    print(Stat.GetINode(target_dummy))
    print(Stat.GetDeviceId(target_dummy))
