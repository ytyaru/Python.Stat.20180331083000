# このソフトウェアについて

ファイルのメタデータ操作クラスを作ってみる。

# 動機

更新時間などを変更するとき、エポックタイム、日付型、文字列(ISO8601等)など形式を意識したくない。

また、osモジュールではファイル作成日時の取得方法がOSごとに異なる。その差分を吸収したい。

os.utime()でアクセス日時と更新日時を指定できるが、同時に指定せねばならない。しかも値が未指定のものは現在時刻で更新されてしまう。未指定のときは現状のままにするようにしたい。

# 他

* [Python.Path.20180329185623](https://github.com/ytyaru/Python.Path.20180329185623)
* [Python.Directory.20180330200129](https://github.com/ytyaru/Python.Directory.20180330200129)

# 参考

* https://msdn.microsoft.com/ja-jp/library/system.io.directory(v=vs.110).aspx
* https://docs.python.jp/3/library/shutil.html
* https://docs.python.jp/3/library/os.html
* https://docs.python.jp/3/library/os.path.html
* https://docs.python.jp/3/library/pathlib.html

# 開発環境

* [Raspberry Pi](https://ja.wikipedia.org/wiki/Raspberry_Pi) 3 Model B
    * [Raspbian](https://www.raspberrypi.org/downloads/raspbian/) GNU/Linux 8.0 (jessie)
        * [pyenv](http://ytyaru.hatenablog.com/entry/2019/01/06/000000)
            * Python 3.6.4

# ライセンス

このソフトウェアはCC0ライセンスである。

[![CC0](http://i.creativecommons.org/p/zero/1.0/88x31.png "CC0")](http://creativecommons.org/publicdomain/zero/1.0/deed.ja)

