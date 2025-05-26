#!/usr/bin/env python
# coding: utf-8

# In[1]:


import csv

with open('Ref/sentimentdataset.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)        
    header = next(reader)         
    print("Columns:", header)


# In[23]:


with open('Ref/sentimentdataset.csv', newline='', encoding='utf-8') as f:
    sample = f.read(2048)
    dialect = csv.Sniffer().sniff(sample, delimiters=[',',';','\t', '|'])
    print(f"Detected delimiter: {repr(dialect.delimiter)}")


# In[25]:


has_header = csv.Sniffer().has_header(sample)
print("Header detected?" , has_header)


# In[88]:


with open('Ref/sentimentdataset.csv', newline='', encoding='utf-8') as f:
    reader = csv.reader(f, dialect)
    header = next(reader)
    for i, row in enumerate(reader):
        if i >= 1: break
        print(row)


# In[90]:


with open('Ref/sentimentdataset.csv', newline='', encoding='utf-8') as f:
    reader = csv.reader(f, dialect)
    header = next(reader)
    for i, row in enumerate(reader):
        if i >= 5: break
        print(f"ID: {row[0]}, TextComment: {row[2].strip()}, Sentiment: {row[3].strip()}")


# In[148]:


with open('Ref/sentimentdataset.csv', newline='', encoding='utf-8') as f:
    reader = csv.reader(f, dialect)
    header = next(reader)
    all_rows = list(reader)


# In[150]:


res_pos = [1 if row[3].strip() == 'Positive' else 0 for row in all_rows]
res_neg = [1 if row[3].strip() == 'Negative' else 0 for row in all_rows]
res_neu = [1 if row[3].strip() == 'Neutral' else 0 for row in all_rows]

print(f"Total number of Positive comments is {sum(res_pos)}")
print(f"Total number of Negative comments is {sum(res_neg)}")
print(f"Total number of Neutral comments is {sum(res_neu)}")


# In[155]:


with open('Ref/sentimentdataset.csv', newline='', encoding='utf-8') as f:
    dict_reader = csv.DictReader(f, dialect=dialect)
    for i, row in enumerate(dict_reader):
        if i >= 2: break
        print(row['Text'], row['Sentiment'])


# In[208]:


INPUT = 'Ref/sentimentdataset.csv'
OUTPUT = 'Ref/quoted_nonnum.csv'

with open(INPUT, newline='', encoding='utf-8') as fin, \
     open(OUTPUT, 'w', newline='', encoding='utf-8') as fout:

    reader = csv.DictReader(fin)
    writer = csv.writer(fout, quoting=csv.QUOTE_NONNUMERIC)
    writer.writerow(['Text', 'Likes'])

    for i, row in enumerate(reader):
        if i >= 5: break
        writer.writerow([ row['Text'].strip() , float(row['Likes']) ])


# In[ ]:


INPUT = 'Ref/sentimentdataset.csv'
OUTPUT = 'Ref/quoted_nonnum.csv'

with open(INPUT, newline='', encoding='utf-8') as fin, \
     open(OUTPUT, 'w', newline='', encoding='utf-8') as fout:

    reader = csv.DictReader(fin)
    writer = csv.writer(fout, quoting=csv.QUOTE_ALL)
    writer.writerow(['Text', 'Likes'])

    for i, row in enumerate(reader):
        if i >= 5: break
        writer.writerow([ row['Text'].strip() , float(row['Likes']) ])

