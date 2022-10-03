from automat import Automat

if __name__ == '__main__':
    automat = Automat(delay = 0.0000001)
    automat.record_process()
    automat.run_process()
