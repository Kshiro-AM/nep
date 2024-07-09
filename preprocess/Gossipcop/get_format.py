import json
import os
import random
from argparse import ArgumentParser
from tqdm import tqdm


if __name__ == '__main__':
    parser = ArgumentParser(description='Get right format from Gossipcop')
    parser.add_argument('--dataset', type=str)
    args = parser.parse_args()
    
    dataset = args.dataset
    origin_file = 'data/{}.json'.format(dataset)
    save_dir = 'data/'
    if not os.path.exists(save_dir):
        os.mkdir(save_dir)
        
    with open(origin_file, 'r') as f:
        pieces = json.load(f)
        
    train = []
    val = []
    test = []
    
    for piece in tqdm(pieces):
        random_num = random.randint(0, 4)
        new_piece = {
            'content': pieces[piece]['text'],
            'label': pieces[piece]['label'],
        }
        if 'article' in pieces[piece]['meta_data'] and 'published_time' in pieces[piece]['meta_data']['article']:
            new_piece['time'] = pieces[piece]['meta_data']['article']['published_time']
        else:
            continue
        
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