import json
import os
import random
import datetime
from argparse import ArgumentParser
from tqdm import tqdm


if __name__ == '__main__':
    parser = ArgumentParser(description='Get right format from Gossipcop')
    args = parser.parse_args()
    
    save_dir = 'data/'
    if not os.path.exists(save_dir):
        os.mkdir(save_dir)
        
    train = []
    val = []
    test = []
    news = []
    
    # origin_dataset
    with open('data/gossipcop_v3_origin.json', 'r') as f:
        origin_pieces = json.load(f)
        for piece in tqdm(origin_pieces):
            new_piece = {
                'content': origin_pieces[piece]['text']
            }
            if 'article' in origin_pieces[piece]['meta_data'] and 'published_time' in origin_pieces[piece]['meta_data']['article']:
                time = origin_pieces[piece]['meta_data']['article']['published_time'][:10]
                try:
                    datetime.datetime.strptime(time, "%Y-%m-%d")
                except:
                    continue
                
                new_piece['date'] = origin_pieces[piece]['meta_data']['article']['published_time'][:10]
            else:
                continue
            
            if origin_pieces[piece]['label'] == 'real':
                news.append(new_piece)
    
    datasets = ['gossipcop_v3-1_style_based_fake.json', 'gossipcop_v3-5_style_based_legitimate.json']
    for file in datasets:
        with open('data/{}'.format(file), 'r') as f:
            pieces = json.load(f)
            for piece in tqdm(pieces):
                try: 
                    text = pieces[piece]['generated_text_t015']
                except:
                    text = pieces[piece]['generated_text']
                new_piece= {
                    'content': text,
                    'label': pieces[piece]['generated_label']
                }
                if new_piece['label'] == 'legitimate':
                    new_piece['label'] = 'real'
                    
                if 'article' in origin_pieces[piece]['meta_data'] and 'published_time' in origin_pieces[piece]['meta_data']['article']:
                    time = origin_pieces[piece]['meta_data']['article']['published_time'][:10]
                    try:
                        datetime.datetime.strptime(time, "%Y-%m-%d")
                    except:
                        continue
                
                    new_piece['time'] = origin_pieces[piece]['meta_data']['article']['published_time'][:10] + ' ' + '00:00:00'
                else:
                    continue
                
                random_num = random.randint(0, 4)
                if random_num == 0:
                    # 20% for test
                    test.append(new_piece)
                elif random_num == 1:
                    # 20% for validation
                    val.append(new_piece)
                else:
                    # 60% for training
                    train.append(new_piece)
                
            
    random.shuffle(train)
    random.shuffle(val)
    random.shuffle(test)
            
    json.dump(train, open(os.path.join(save_dir, 'train.json'), 'w'), ensure_ascii=False)
    json.dump(val, open(os.path.join(save_dir, 'val.json'), 'w'), ensure_ascii=False)
    json.dump(test, open(os.path.join(save_dir, 'test.json'), 'w'), ensure_ascii=False)
    json.dump(news, open(os.path.join(save_dir, 'news.json'), 'w'), ensure_ascii=False)