import sys, os, os.path, pathlib
sys.path.append(str(pathlib.Path(__file__).parent.parent / 'src'))
from Stat import Stat
import unittest
import time, datetime

class StatTest(unittest.TestCase):
    def __MakeDummy(self, path, size):
        os.makedirs(os.path.dirname(path), exist_ok=True)
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

    def test_ModifiedDateTime_Get_Set(self):
        target_root = '/tmp/work/__TEST__'
        target_dummy = os.path.join(target_root, 'a.dummy')
        self.__MakeDummy(target_dummy, 1024)

        self.assertTrue(tuple == type(Stat.GetModifiedDateTime(target_dummy)))
        self.assertTrue(2 == len(Stat.GetModifiedDateTime(target_dummy)))
        self.assertTrue(float == type(Stat.GetModifiedDateTime(target_dummy)[0]))
        self.assertTrue(datetime.datetime == type(Stat.GetModifiedDateTime(target_dummy)[1]))
        #print(type(Stat.GetModifiedDateTime(target_dummy)[0]))
        #print(type(Stat.GetModifiedDateTime(target_dummy)[1]))
        dt1 = datetime.datetime.strptime('1999/12/31 23:59:59', '%Y/%m/%d %H:%M:%S')
        dt2 = datetime.datetime.strptime('2345/01/02 12:34:56', '%Y/%m/%d %H:%M:%S')
        epoch, dt = Stat.GetModifiedDateTime(target_dummy)
        self.assertTrue(dt1 != dt)
        self.assertTrue(dt2 != dt)
        
        Stat.SetModifiedDateTime(target_dummy, dt1)
        self.assertTrue(int(time.mktime(dt1.timetuple())) == Stat.GetModifiedDateTime(target_dummy)[0])
        self.assertTrue(dt1 == Stat.GetModifiedDateTime(target_dummy)[1])
        self.assertTrue(dt1 != Stat.GetChangedMetaDataDateTime(target_dummy)[1])
        self.assertTrue(dt1 != Stat.GetAccessedDateTime(target_dummy)[1])
        os.remove(target_dummy)

    def test_AccessedDateTime_Get_Set(self):
        target_root = '/tmp/work/__TEST__'
        target_dummy = os.path.join(target_root, 'a.dummy')
        self.__MakeDummy(target_dummy, 1024)

        self.assertTrue(tuple == type(Stat.GetAccessedDateTime(target_dummy)))
        self.assertTrue(2 == len(Stat.GetAccessedDateTime(target_dummy)))
        self.assertTrue(float == type(Stat.GetAccessedDateTime(target_dummy)[0]))
        self.assertTrue(datetime.datetime == type(Stat.GetAccessedDateTime(target_dummy)[1]))
        dt1 = datetime.datetime.strptime('1999/12/31 23:59:59', '%Y/%m/%d %H:%M:%S')
        dt2 = datetime.datetime.strptime('2345/01/02 12:34:56', '%Y/%m/%d %H:%M:%S')
        epoch, dt = Stat.GetAccessedDateTime(target_dummy)
        self.assertTrue(dt1 != dt)
        self.assertTrue(dt2 != dt)
        
        Stat.SetAccessedDateTime(target_dummy, dt1)
        self.assertTrue(int(time.mktime(dt1.timetuple())) == Stat.GetAccessedDateTime(target_dummy)[0])
        self.assertTrue(dt1 == Stat.GetAccessedDateTime(target_dummy)[1])
        self.assertTrue(dt1 != Stat.GetModifiedDateTime(target_dummy)[1])
        self.assertTrue(dt1 != Stat.GetChangedMetaDataDateTime(target_dummy)[1])
        os.remove(target_dummy)

    def test_GetChangedMetaDataDateTime(self):
        target_root = '/tmp/work/__TEST__'
        target_dummy = os.path.join(target_root, 'a.dummy')
        self.__MakeDummy(target_dummy, 1024)

        print(Stat.GetChangedMetaDataDateTime(target_dummy))
        print(Stat.GetCreatedDateTime(target_dummy))
        os.remove(target_dummy)

    def test_Ids(self):
        target_root = '/tmp/work/__TEST__'
        target_dummy = os.path.join(target_root, 'a.dummy')
        self.__MakeDummy(target_dummy, 1024)
        print(Stat.GetOwnUserId(target_dummy))
        print(Stat.GetOwnGroupId(target_dummy))
        print(Stat.GetHardLinkNum(target_dummy))
        print(Stat.GetINode(target_dummy))
        print(Stat.GetDeviceId(target_dummy))


if __name__ == '__main__':
    unittest.main()
