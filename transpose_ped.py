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
    def __init__(self, row):
        self.family_id = row[1]
        self.individual_id = row[2]
        self.father_id = row[3]
        self.mother_id = row[4]
        self.sex = row[5]
        self.status = row[6]
        self.alleles = []


class Storage(object):
    """Storage class with merge methods"""

    def __init__(self):
        self.snp_store = []
        self.ped_store = []

    def phenoscanner_to_bolt(self, bolt_record):
        """
      Links Phenoscanner results to the relevant Bolt-LMM object
      """
        filtered_list = [ps for ps in self.ps_store if
                         ((ps.chromosome == bolt_record.chromosome) and (ps.coordinate == bolt_record.coordinate))]
        print(filtered_list)


class MapParser(object):
    """
   MAP file parser
    """

    def read_bolt(self, file_path, storage):
        """
      Reads in MAP text file, with SNP information
      Args:
         file_path (str): Given filepath to MAP file
      Returns:
         storage : A Storage object with a List of MAP file rows
        """

        with open(file_path) as map_file:
            tsv_reader = csv.DictReader(map_file, delimiter="\t")
            for row in tsv_reader:
                this_snp = Snp(row)
                storage.snp_store.append(this_snp)
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
        parser.add_argument('--test')
        args = parser.parse_args()


if __name__ == '__main__':
    Main()
