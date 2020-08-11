'''data = DdsFormat.Data()
from tempfile import TemporaryFile
stream = TemporaryFile()
data.write(stream)'''

job_keys = [12, 13, 15, 28]
amounts = [12, 14, 100, 50]
batchsizes = [12, 14, 50, 50]
articles = [1, 2, 3, 4]



def write_job_dds(file, job_key, amount, batchsize, article):
    # нужно подтянуть ArticleKey, зная AricleID
    file.write('[NewJob] '
               '\nJob = ABC, {job_key} '
               '\nArticleKey = {article_id} '
               '\nTotalPieces = {total_pieces} '
               '\nBatchSize = {batch} '
               '\nName = "Leadset{job_key}"'.format(job_key = job_key, article_id = article, total_pieces = amount, batch = batchsize))



def  __add_1_ARTICLE(self, job_key, amount, batchsize, article):
    """
    Func prepares data to Article.dds file
    """
    '[NewJob] '
    '\nJob = ABC, {job_key} '
    '\nArticleKey = {article_id} '
    '\nTotalPieces = {total_pieces} '
    '\nBatchSize = {batch} '
    '\nName = "Leadset{job_key}"'.format(job_key=job_key, article_id=article, total_pieces=amount, batch=batchsize)
    '' \
    '\n[NewArticle]' \
    '\nArticleKey = {article_key}' \
    '\nNumberOfLeadSets = 1' \
    '\n' \
    '\n[NewLeadSet1]' \
    '\nWireKey = {wire_key}' \
    '\nWireLength = {wire_length}' \
 \
 \
 \
#file = open("file.dds", "w")
dds_files_path = 'C:\Komax\Data\WPCS-Data\{}'






file = open(dds_files_path.format("file.txt"), "w")
write_job_dds(file, 12, 13, '', 1)
file.close()

'''def add_1_ARTICLE(job_key):
    """
    Func prepares data to Article.dds file
    """
    return '\n' \
            '\n[NewJob]' \
            '\nJob = ABC, {job_key}' \
            '\nArticleKey = {article_id}' \
            '\nTotalPieces = {total_pieces}' \
            '\n' \
            '\n[NewLeadSet1]' \
            '\nWireKey = {job_key}' \
            '\nWireLength = {total_pieces}'.format(job_key=job_key, article_id=job_key, total_pieces=job_key)


for_writing_DDS = ''
for job_key in job_keys:
    for_writing_DDS += add_1_ARTICLE(job_key)

print(for_writing_DDS)

#file = open("file.dds", "w")
dds_files_path = 'C:\Komax\Data\WPCS-Data\{}'




file = open(dds_files_path.format("file.txt"), "w")
file.write(for_writing_DDS)
#write_job_dds(file, 12, 13, '', 1)
file.close()'''

#file = open("file.dds", "w")
#file.write("test test")
#file.close()

file = open("file.txt", "r")
data = file.read()
print(data)
file.close()

