"""
Main entry point for the transpose_ped parser.
"""
import argparse
import csv


class Snp(object):
    def __init__(self, row):
        self.chromosome = row[1]
        self.marker_id = row[2]
        self.genetic_distance = row[3]
        self.position = row[4]


class Alleles(object):
    def __init__(self, row):
        self.alleles = [row]


class Individual(object):
    def __init__(self, row, storage):
        self.family_id = row[1]
        self.individual_id = row[2]
        self.father_id = row[3]
        self.mother_id = row[4]
        self.sex = row[5]
        self.status = row[6]

        #marker_names = storage.snp_store
        self.alleles = []


class Storage(object):
    """Storage class with merge methods"""

    def __init__(self):
        self.snp_store = []
        self.ped_store = []


class MapParser(object):
    """
   MAP file parser
    """

    def read_map(self, file_path, storage):
        """
      Reads in MAP text file, with SNP information
      Args:
         file_path (str): Given filepath to MAP file
      Returns:
         storage : A Storage object with a List of MAP file rows
         :param file_path:
         :param storage:
        """

        with open(file_path) as map_file:
            tsv_reader = csv.DictReader(map_file, delimiter="\t")
            for row in tsv_reader:
                this_snp = Snp(row)
                storage.snp_store.append(this_snp)
        return storage


class PedParser(object):
    """
   PED file parser
    """

    def read_ped(self, file_path, storage):
        """
      Reads in MAP text file, with SNP information
      Args:
         file_path (str): Given filepath to MAP file
      Returns:
         storage : A Storage object with a List of MAP file rows
         :param file_path:
         :param storage:
        """

        with open(file_path) as ped_file:
            tsv_reader = csv.DictReader(ped_file, delimiter="\t")
            for row in tsv_reader:
                this_individual = Individual(row, storage)
                storage.ped_store.append(this_individual)
        return storage


class Main(object):
    """
   Main class
    """

    def __init__(self):
        parser = argparse.ArgumentParser(description='Transpose PED files')
        parser.add_argument('-m', '--map_path', dest='map_path',
                            help='MAP file to be parsed', required=True)
        parser.add_argument('-p', '--ped_path', dest='ped_path',
                            help='PED file to be merged and transposed', required=True)
        parser.add_argument('-fp', '--fam_prefix', dest='fam_prefix',
                            help='Family prefix')
        parser.add_argument('-s', '--status_change', dest='status_change',
                            help='Change individual status')
        parser.add_argument('-sx', '--status_change_except', dest='status_change_except',
                            help='Change status except these individual ids')
        parser.add_argument('--test')
        args = parser.parse_args()
        map_reader = MapParser()
        ped_reader = PedParser()
        storage = Storage()

        map_reader.read_map(args.map_path, storage)

        ped_reader.read_ped(args.ped_path, storage)


if __name__ == '__main__':
    Main()
