from Bio import SeqIO
from Bio.Seq import Seq, UnknownSeq, Alphabet
from Bio.SeqFeature import SeqFeature, FeatureLocation
from Bio.SeqRecord import SeqRecord
import sys
import os

from merge_gbk_records import __version__






def merge(records):
    """Merge multiple SeqRecords into one, using a defined spacer

    :param records: Iterable containing SeqRecords to be merged
    :param length: Length of the spacer in kbp
    :param spacer: Kind of spacer to use ('n' for UnknownSeq spacer, 'stop' for all-frame stop codon spacer)

    :return: A single SeqRecord that is the product of the merge.
    """
    length=20
    spacer='n'

    if spacer not in ('n', 'stop'):
        raise ValueError(
            "Invalid spacer: %r, use either 'n' or 'stop'" % spacer)

    if not len(records):
        raise ValueError("No records given")

    if spacer == 'stop':
        spacer_seq = Seq(ALL_FRAME_STOP_MOTIF * 40 *
                         length, Alphabet.generic_dna)
    else:
        spacer_seq = UnknownSeq(
            length * 1000, alphabet=Alphabet.generic_dna, character='N')

    new_rec = records[0]

    if len(records) == 1:
        return new_rec

    
    rec_id = new_rec.id
    rec_name = new_rec.name
    rec_desc = new_rec.description
    date = new_rec.annotations.get('date', '')
    source = new_rec.annotations.get("source", '')
    organism = new_rec.annotations.get('organism', '')
    taxonomy = new_rec.annotations.get('taxonomy', [])
    data_file_division = new_rec.annotations.get('data_file_division', 'UNK')
    topology = new_rec.annotations.get('topology', 'linear')

    for i, rec in enumerate(records[1:]):
        spacer_id = 'spacer_{}'.format(i + 1)

        spacer_feature = SeqFeature(FeatureLocation(0, length * 1000, 0),
                                    type='misc_feature', id=spacer_id,
                                    qualifiers={'note': [spacer_id]})

        spacer_rec = SeqRecord(spacer_seq, id=spacer_id, name=spacer_id,
                               description=spacer_id, features=[spacer_feature])

        new_rec = new_rec + spacer_rec + rec

    new_rec.id = rec_id
    new_rec.name = rec_name
    new_rec.description = rec_desc
    new_rec.annotations["date"] = date
    new_rec.annotations["source"] = source
    new_rec.annotations["organism"] = organism
    new_rec.annotations["taxonomy"] = taxonomy
    new_rec.annotations["data_file_division"] = data_file_division
    new_rec.annotations["topology"] = topology

    return new_rec


ALL_FRAME_STOP_MOTIF = 'TAGCTAACTGACCGTCAGTTAGCTA'

genomesFolder = 'D://downloads//Study//laboratory//EloE//data//downloaded//for_pax-db//' 
genomes = os.listdir(genomesFolder)

for genomeFolder in genomes:
    path = genomesFolder+ '//' + genomeFolder
    contents = os.listdir(path)
    records = []

    print(path)

    #склеивает геномные карточки, лежащие в одной папке
    for genome in contents:
        records.extend(SeqIO.parse(path + '//'+genome, 'genbank'))
    merged_record = merge(records)

    merged_file = "D:\\downloads\\Study\\laboratory\\EloE\\data\\downloaded\\for_pax-db_merged\\" + genomeFolder
    os.mkdir(merged_file)
    outfile = open(merged_file+'\\'+genome, 'w')


    SeqIO.write([merged_record], outfile, 'genbank')