import threading
import Chanke
import Erke
import Fuke
import Nanke
import Neike
import Pifuke
import Waike
import Wuguanke
import Xingbingke


def thread_main():
    # create several threads to get the info simultaneously
    nanke = threading.Thread(target=Nanke.main())
    fuke = threading.Thread(target=Fuke.main())
    neike = threading.Thread(target=Neike.main())
    waike = threading.Thread(target=Waike.main())
    pifuke = threading.Thread(target=Pifuke.main())
    wuguanke = threading.Thread(target=Wuguanke.main())
    chanke = threading.Thread(target=Chanke.main())
    erke = threading.Thread(target=Erke.main())
    xing = threading.Thread(target=Xingbingke.main())

    nanke.start()
    fuke.start()
    neike.start()
    waike.start()
    pifuke.start()
    wuguanke.start()
    chanke.start()
    erke.start()
    xing.start()


if __name__ == '__main__':
    thread_main()
