import sys, os, os.path, pathlib
sys.path.append(str(pathlib.Path(__file__).parent.parent / 'src'))
from Stat import Stat
import unittest
import time, datetime

class StatTest(unittest.TestCase):
    def __MakeDummy(self, path, size):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        if os.path.isfile(path): os.remove(path) # メタデータ初期化
        with open(path, 'wb') as f:
            f.write(b'\0'*size)
    # ----------------------------
    # クラスメソッド
    # ----------------------------
    def test_GetSize(self):
        target_root = '/tmp/work/__TEST__'
        target_dummy = os.path.join(target_root, 'a.dummy')
        self.__MakeDummy(target_dummy, 1024)
        self.assertEqual(1024, Stat.GetSize(target_dummy))

    def test_DiskUsage(self):
        target_root = '/tmp/work/__TEST__'
        target_dummy = os.path.join(target_root, 'a.dummy')
        self.__MakeDummy(target_dummy, 1024)
        self.assertTrue(hasattr(Stat, 'DiskUsage'))
        res = Stat.DiskUsage(target_dummy)
        self.assertTrue(hasattr(res, 'total'))
        self.assertTrue(hasattr(res, 'used'))
        self.assertTrue(hasattr(res, 'free'))
        print(Stat.DiskUsage(target_dummy))

    def test_Mode_Get_Set_Name(self):
        target_root = '/tmp/work/__TEST__'
        target_dummy = os.path.join(target_root, 'a.dummy')
        self.__MakeDummy(target_dummy, 1024)
        mode = Stat.GetMode(target_dummy)
        print(mode)
        print(oct(mode))
        Stat.SetMode(target_dummy, 0o755)
        self.assertEqual(0o100755, Stat.GetMode(target_dummy))
        self.assertEqual('-rwxr-xr-x', Stat.GetModeName(target_dummy))
        Stat.SetMode(target_dummy, '-rwxrwxrwx')
        self.assertEqual(0o100777, Stat.GetMode(target_dummy))
        Stat.SetMode(target_dummy, 0o644)
        self.assertEqual(0o100644, Stat.GetMode(target_dummy))
        self.assertEqual('-rw-r--r--', Stat.GetModeName(target_dummy))

    def test_SetModeFromName_Error(self):
        target_root = '/tmp/work/__TEST__'
        target_dummy = os.path.join(target_root, 'a.dummy')
        self.__MakeDummy(target_dummy, 1024)
        mode_name = 'Invalid-Text'
        with self.assertRaises(ValueError) as e:
            Stat.SetMode(target_dummy, mode_name )
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
        self.assertEqual('引数mode_nameが不正値です。\'{}\'。\'-rwxrwxrwx\'の書式で入力してください。owner, group, other, の順に次のパターンのいずれかを指定します。pattern={}。r,w,xはそれぞれ、読込、書込、実行の権限です。-は権限なしを意味します。'.format(mode_name, mode_names), e.exception.args[0])

    def test_Modified_Get_Set(self):
        target_root = '/tmp/work/__TEST__'
        target_dummy = os.path.join(target_root, 'a.dummy')
        self.__MakeDummy(target_dummy, 1024)

        self.assertTrue(tuple == type(Stat.GetModified(target_dummy)))
        self.assertTrue(2 == len(Stat.GetModified(target_dummy)))
        self.assertTrue(float == type(Stat.GetModified(target_dummy)[0]))
        self.assertTrue(datetime.datetime == type(Stat.GetModified(target_dummy)[1]))
        #print(type(Stat.GetModified(target_dummy)[0]))
        #print(type(Stat.GetModified(target_dummy)[1]))
        dt1 = datetime.datetime.strptime('1999/12/31 23:59:59', '%Y/%m/%d %H:%M:%S')
        dt2 = datetime.datetime.strptime('2345/01/02 12:34:56', '%Y/%m/%d %H:%M:%S')
        epoch, dt = Stat.GetModified(target_dummy)
        self.assertTrue(dt1 != dt)
        self.assertTrue(dt2 != dt)
        
        Stat.SetModified(target_dummy, dt1)
        self.assertTrue(int(time.mktime(dt1.timetuple())) == Stat.GetModified(target_dummy)[0])
        self.assertTrue(dt1 == Stat.GetModified(target_dummy)[1])
        self.assertTrue(dt1 != Stat.GetChangedMeta(target_dummy)[1])
        self.assertTrue(dt1 != Stat.GetAccessed(target_dummy)[1])

    def test_Accessed_Get_Set(self):
        target_root = '/tmp/work/__TEST__'
        target_dummy = os.path.join(target_root, 'a.dummy')
        self.__MakeDummy(target_dummy, 1024)

        self.assertTrue(tuple == type(Stat.GetAccessed(target_dummy)))
        self.assertTrue(2 == len(Stat.GetAccessed(target_dummy)))
        self.assertTrue(float == type(Stat.GetAccessed(target_dummy)[0]))
        self.assertTrue(datetime.datetime == type(Stat.GetAccessed(target_dummy)[1]))
        dt1 = datetime.datetime.strptime('1999/12/31 23:59:59', '%Y/%m/%d %H:%M:%S')
        dt2 = datetime.datetime.strptime('2345/01/02 12:34:56', '%Y/%m/%d %H:%M:%S')
        epoch, dt = Stat.GetAccessed(target_dummy)
        self.assertTrue(dt1 != dt)
        self.assertTrue(dt2 != dt)
        
        Stat.SetAccessed(target_dummy, dt1)
        self.assertTrue(int(time.mktime(dt1.timetuple())) == Stat.GetAccessed(target_dummy)[0])
        self.assertTrue(dt1 == Stat.GetAccessed(target_dummy)[1])
        self.assertTrue(dt1 != Stat.GetModified(target_dummy)[1])
        self.assertTrue(dt1 != Stat.GetChangedMeta(target_dummy)[1])

    def test_GetChangedMeta(self):
        target_root = '/tmp/work/__TEST__'
        target_dummy = os.path.join(target_root, 'a.dummy')
        self.__MakeDummy(target_dummy, 1024)
        self.assertTrue(hasattr(Stat, 'GetChangedMeta'))
        self.assertTrue(hasattr(Stat, 'GetCreated'))
        print(Stat.GetChangedMeta(target_dummy))
        print(Stat.GetCreated(target_dummy))

    def test_Ids(self):
        target_root = '/tmp/work/__TEST__'
        target_dummy = os.path.join(target_root, 'a.dummy')
        self.__MakeDummy(target_dummy, 1024)
        self.assertTrue(hasattr(Stat, 'OwnUserId'))
        self.assertTrue(hasattr(Stat, 'OwnGroupId'))
        self.assertTrue(hasattr(Stat, 'HardLinkNum'))
        self.assertTrue(hasattr(Stat, 'INode'))
        self.assertTrue(hasattr(Stat, 'DeviceId'))
        print(Stat.GetOwnUserId(target_dummy))
        print(Stat.GetOwnGroupId(target_dummy))
        print(Stat.GetHardLinkNum(target_dummy))
        print(Stat.GetINode(target_dummy))
        print(Stat.GetDeviceId(target_dummy))

    # ----------------------------
    # インスタンスメソッド
    # ----------------------------
    def test_Stat(self):
        target_root = '/tmp/work/__TEST__'
        target_dummy = os.path.join(target_root, 'a.dummy')
        self.__MakeDummy(target_dummy, 1024)

        s = Stat(target_dummy)
        self.assertEqual(Stat, type(s))
        self.assertEqual(os.stat_result, type(s.Stat))

    def test_Path(self):
        target_root = '/tmp/work/__TEST__'
        target_dummy = os.path.join(target_root, 'a.dummy')
        self.__MakeDummy(target_dummy, 1024)

        s = Stat(target_dummy)
        self.assertEqual('/tmp/work/__TEST__/a.dummy', s.Path)

    def test_Size(self):
        target_root = '/tmp/work/__TEST__'
        target_dummy = os.path.join(target_root, 'a.dummy')
        self.__MakeDummy(target_dummy, 1024)

        s = Stat(target_dummy)
        self.assertEqual(1024, s.Size)

    def test_Mode(self):
        target_root = '/tmp/work/__TEST__'
        target_dummy = os.path.join(target_root, 'a.dummy')
        self.__MakeDummy(target_dummy, 1024)

        s = Stat(target_dummy)
        s.Mode = 0o777
        self.assertEqual(0o100777, s.Mode)
        self.assertEqual('-rwxrwxrwx', s.ModeName)
        s.Mode = 0o644
        self.assertEqual(0o100644, s.Mode)
        self.assertEqual('-rw-r--r--', s.ModeName)
        s.Mode = '-rwxrwxrwx'
        self.assertEqual(0o100777, s.Mode)
        self.assertEqual('-rwxrwxrwx', s.ModeName)

    def test_Modified(self):
        target_root = '/tmp/work/__TEST__'
        target_dummy = os.path.join(target_root, 'a.dummy')
        self.__MakeDummy(target_dummy, 1024)

        s = Stat(target_dummy)
        self.assertTrue(tuple == type(s.Modified))
        self.assertTrue(2 == len(s.Modified))
        self.assertTrue(float == type(s.Modified[0]))
        self.assertTrue(datetime.datetime == type(s.Modified[1]))
        dt1 = datetime.datetime.strptime('1999/12/31 23:59:59', '%Y/%m/%d %H:%M:%S')
        dt2 = datetime.datetime.strptime('2345/01/02 12:34:56', '%Y/%m/%d %H:%M:%S')
        epoch, dt = s.Modified
        self.assertTrue(dt1 != dt)
        self.assertTrue(dt2 != dt)
        
        s.Modified = dt1
        self.assertTrue(int(time.mktime(dt1.timetuple())) == s.Modified[0])
        self.assertTrue(dt1 == s.Modified[1])
        self.assertTrue(dt1 != s.Accessed[1])
        self.assertTrue(dt1 != s.Created[1])
        self.assertTrue(dt1 != s.ChangedMeta[1])

    def test_Accessed(self):
        target_root = '/tmp/work/__TEST__'
        target_dummy = os.path.join(target_root, 'a.dummy')
        self.__MakeDummy(target_dummy, 1024)

        s = Stat(target_dummy)
        self.assertTrue(tuple == type(s.Accessed))
        self.assertTrue(2 == len(s.Accessed))
        self.assertTrue(float == type(s.Accessed[0]))
        self.assertTrue(datetime.datetime == type(s.Accessed[1]))
        dt1 = datetime.datetime.strptime('1999/12/31 23:59:59', '%Y/%m/%d %H:%M:%S')
        dt2 = datetime.datetime.strptime('2345/01/02 12:34:56', '%Y/%m/%d %H:%M:%S')
        epoch, dt = s.Accessed
        self.assertTrue(dt1 != dt)
        self.assertTrue(dt2 != dt)
        
        s.Accessed = dt1
        self.assertTrue(int(time.mktime(dt1.timetuple())) == s.Accessed[0])
        self.assertTrue(dt1 == s.Accessed[1])
        self.assertTrue(dt1 != s.Modified[1])
        self.assertTrue(dt1 != s.Created[1])
        self.assertTrue(dt1 != s.ChangedMeta[1])

    def test_ChangedMeta(self):
        target_root = '/tmp/work/__TEST__'
        target_dummy = os.path.join(target_root, 'a.dummy')
        self.__MakeDummy(target_dummy, 1024)
        s = Stat(target_dummy)
        self.assertTrue(hasattr(s, 'ChangedMeta'))
        self.assertTrue(hasattr(s, 'Created'))
        print(s.ChangedMeta)
        print(s.Created)

    def test_Ids_Property(self):
        target_root = '/tmp/work/__TEST__'
        target_dummy = os.path.join(target_root, 'a.dummy')
        self.__MakeDummy(target_dummy, 1024)
        s = Stat(target_dummy)
        self.assertTrue(hasattr(s, 'OwnUserId'))
        self.assertTrue(hasattr(s, 'OwnGroupId'))
        self.assertTrue(hasattr(s, 'HardLinkNum'))
        self.assertTrue(hasattr(s, 'INode'))
        self.assertTrue(hasattr(s, 'DeviceId'))
        print(s.OwnUserId)
        print(s.OwnGroupId)
        print(s.HardLinkNum)
        print(s.INode)
        print(s.DeviceId)


if __name__ == '__main__':
    unittest.main()
