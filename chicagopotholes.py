import csv
import urllib.request
import re

# Find the five most post-apocalyptic pothole-filled 10-block section of road in Chicago
# Bonus: identify the worst road based on data involving number of patched potholes

def main():
    #url = 'https://data.cityofchicago.org/api/views/7as2-ds3y/rows.csv'#?accessType=DOWNLOAD'
    fname = 'potholes.csv'
    #urllib.request.urlretrieve(url, fname)
    xfile = open(fname, 'r')
    reader = csv.DictReader(xfile)
    block_pothole_lst = []
    for row in reader:
        lst = []
        if row['NUMBER OF POTHOLES FILLED ON BLOCK'] != '':
            block_no = (re.search(r'(\d+) ([ \w]+)', row['STREET ADDRESS'])).group(1)
            block_street = (re.search(r'(\d+) ([ \w]+)', row['STREET ADDRESS'])).group(2)
            block = int(float(block_no)/100) * 100
            addr = str(block) + ' ' + block_street
            filled = float(row['NUMBER OF POTHOLES FILLED ON BLOCK'])
            if filled > 0:
                lst.append(block_street)
                lst.append(block)
                lst.append(filled)
                block_pothole_lst.append(lst)
    aveneue_pothole_dict = {}
    for block in block_pothole_lst:
        addr = block[0]
        filled = block[2]
        if addr in aveneue_pothole_dict:
            aveneue_pothole_dict[addr] = aveneue_pothole_dict[addr] + filled
        else:
            aveneue_pothole_dict[addr] = filled
    def sort_key(key):
        return aveneue_pothole_dict[key[0]]
    aveneue_pothole_dict_sort = sorted(aveneue_pothole_dict.items(), key=sort_key, reverse=True)
    aveneue_pothole_top_ten = aveneue_pothole_dict_sort[:10])


if __name__ == '__main__':
    main()


'''
addresses on the same road
100 -> 1000
add up potholes on first 10 blocks and get a total
add the next block and subtract the first block
if that first total is greater than second total
keep total, else replace total
keep the last block location so that you can recalc the previous ten blocks
once the street is finished
the worst 10 block might be < 10 blocks b/c roads might not be represented
    pothole_dict = {}
    for row in pothole_lst:
    addr = row[0]
    holes  = row[1]
    if addr in pothole_dict:
        pothole_dict[addr] = pothole_dict[addr] + holes
    else:
        pothole_dict[addr] = holes
    for row in pothole_lst:
        if row in block_pothole_lst[0]:
            if row[0] in block_pothole_lst:
            index = block_pothole_lst.index(row[0])
            block_pothole_lst([index][1]) = block_pothole_lst([index][1]) + row[1]
        else:
            block_pothole_lst.append(row)
'''
