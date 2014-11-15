#!/usr/bin/python

import glob
import os
import argparse
import hashlib
import common
import time

current_milli_time = lambda: int(round(time.time() * 1000))

class FileInfo(object):
    print_short = False

    def __init__(self, full_path, checksum_size_kb = 1000):
        self.full_path = full_path
        statinfo = os.stat(full_path)
        self.size = statinfo.st_size
        self.time = statinfo.st_mtime
        self.checksum = None
        self.checksum_size_kb = checksum_size_kb
        pass

    def __cmp__(self, other):
        assert isinstance(other, FileInfo) # assumption for this example
        return cmp(self.full_path, other.full_path)

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        if FileInfo.print_short:
            return self.full_path
        else:
            s = 'FileInfo(' + self.full_path + ', size=' + str(self.size) + ', time=' + str(self.time) 
            if not self.checksum is None:
                s += ', checksum'
            s += ')'
            return s

    def get_checksum(self):
        if self.checksum is None:
            self.gen_checksum()
        return self.checksum

    def gen_checksum(self):
        f = open(self.full_path, 'rb')
        data = f.read(self.checksum_size_kb*1024)
        if self.size > len(data) and len(data) < (9*self.checksum_size_kb*1024)/10 :
            print "expected " + str(self.checksum_size_kb) + " kb, got " + str(len(data)/1024) + "kb on file " + self.full_path
        self.checksum = hashlib.md5(data).digest()
        f.close()
        return self.checksum

class DupFinder(object):
    """description of class"""


    def __init__(self):
        self.files = []
        self.by_size = {}
        self.by_hash = {}
        pass


    def find_all_files(self):
        if len(self.files)>0:
            return # already done
        if not common.is_iterable(self.root_dir):
            self.root_dir = [self.root_dir]
        
        for root in self.root_dir:
            t0 = current_milli_time()
            walk = os.walk(root)
            t1 = current_milli_time()
            if not self.dump_dups and t1-t0 > 1000:
                print "os.walk took " + str(t1-t0) + " ms"
            for root, dirs, files in walk:
                for file in files:
                    full_path = os.path.join(root, file)
                    # print "examine: " + full_path
                    f = FileInfo(full_path, self.checksum_size_kb)
                    if self.use_checksum:
                        f.gen_checksum()
                    self.files.append(f)
                    l = len(self.files)
                    if not self.dump_dups and (l % 100) == 0:
                        print 'processed ' + str(l) + ' files'


        for fi in self.files:
            if fi.size < self.min_size:
                continue
            self.by_size.setdefault(fi.size, []).append(fi)
            #self.by_hash.setdefault(fi.checksum, []).append(fi)

    def get_dups(self):
        self.dups = []
        for size, files in self.by_size.items():
            if len(files) < 2:
                continue
            # print 'same size: ' + str(files)
            for fi in files:
                fi.gen_checksum()
                self.by_hash.setdefault(fi.checksum, []).append(fi)
                
        for hash, files in self.by_hash.items():
            if len(files) < 2:
                continue
            #print 'same hash: ' + str(files)
            self.dups.append(files)

        self.dups = common.sort_and_deduplicate(self.dups)
        return self.dups

    def main(self):
        self.find_all_files()
   
        FileInfo.print_short = True
        if not self.dump_dups:
            print "Total of " + str(len(self.files)) + " files"
            print self.files
            print "##########################"

   
        self.get_dups()

        for dup in self.dups:
            filenames = map(lambda fi: fi.full_path, dup)
            filenames.sort()

            if self.dump_dups:
                for f in filenames[1:]:
                    print f
            else:
                s =  str(len(dup)) + ' dups '
                if dup[0].size == dup[1].size:
                    s += 'same size '
                if not dup[0].checksum is None and dup[0].checksum == dup[1].checksum:
                    s += 'same checksum '

                for f in filenames:
                    s += '\n    ' + f 
                print s

        #print self.dups
        pass


if __name__ == '__main__':
    #print "dupfinder"
    
    parser = argparse.ArgumentParser(description='My favorite argparser.')
    parser.add_argument('path', help='path to search', default='.', nargs='*')
    parser.add_argument('--checksums', help='should checksums be used (slow)', action='store_true', default=False, required=False)
    parser.add_argument('--min-size', help='min-size for files (kb)', dest='min_size', default=0, type=int)
    parser.add_argument('--checksum-size', help='number of kb to use for checksum ', dest='checksum_size_kb', default=10, type=int)
    parser.add_argument('--dump-dups', help='prints only the duplicates (second to n:th file)', dest='dump_dups', action='store_true', default=False, required=False)

                
    args = parser.parse_args()

    # common.tracelevel = args.tracelevel

    dp = DupFinder()
    dp.root_dir = args.path
    dp.use_checksum = args.checksums
    dp.min_size = 1024*args.min_size
    dp.checksum_size_kb = args.checksum_size_kb
    dp.dump_dups = args.dump_dups
    dp.main()




