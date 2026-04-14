import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/media/kim/f1277ab9-8a55-4744-9d16-761b793c0e9e/home/kim/Bachelor_Thesis/Bachelor-Thesis/install/space_printer_core'
