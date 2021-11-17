import timm
import os
import torch
from tqdm import tqdm
from timm.data import resolve_data_config
from timm.data.transforms_factory import create_transform
from PIL import Image

dic = {
    'test2017': 'test2017', 
    'testcoco': 'testcoco',
    'test2016': 'flickr30k',
    'train': 'flickr30k',
    'val': 'flickr30k',
    }

dic2 = {
    'test2017': 'test1', 
    'testcoco': 'test2',
    'test2016': 'test',
    'train': 'train',
    'val': 'valid',
    }

data_splits = ['train', 'val', 'test2016', 'test2017', 'testcoco']

dic_model = [
    'vit_tiny_patch16_384',
    'vit_small_patch16_384',
    'vit_base_patch16_384',
    'vit_large_patch16_384',
]

def get_filenames(path):
    l = []
    with open(path, 'r') as f:
        for line in f:
            l.append(line.strip().split('#')[0])
    return l

if __name__ == "__main__":
    # please see scripts/README.md firstly. 
    flickr30k_path = '../flickr30k'
    dataset = data_splits[-1]
    model_name = dic_model[0]
    save_dir = os.path.join('data', model_name)
    
    if not os.path.exists(save_dir):
        os.mkdir(save_dir)
    
    model = timm.create_model(model_name, pretrained=True, num_classes=0).to('cuda:0') # if use cpu, uncomment '.to('cuda:0')'
    model.eval()
    config = resolve_data_config({}, model=model)
    transform = create_transform(**config)

    tmp = []
    count = 1

    filenames = get_filenames(os.path.join(flickr30k_path, dataset+'_images.txt'))
    
    with torch.no_grad():
        for i in tqdm(filenames):
            i = os.path.join(flickr30k_path, dic[dataset]+'-images', i)
            img = Image.open(i).convert("RGB")
            input = transform(img).unsqueeze(0).to('cuda:0') # transform and add batch dimension
            
            out = model.forward_features(input)
            print(out.shape)
            exit()
            tmp.append(out.detach().to('cuda:1'))
            if len(tmp) == 2000:
                res = torch.cat(tmp).cpu()
                print(res.shape)
                torch.save(res, os.path.join(save_dir, str(count)+dic2[dataset]+'.pth'))
                count += 1
                tmp = []
    
    res = torch.cat(tmp).cpu()
    print(dataset, res.shape, 'save in: ', save_dir)
    if count > 1:
        torch.save(res, os.path.join(save_dir, 'final'+dic2[dataset]+'.pth'))
    else:
        torch.save(res, os.path.join(save_dir, dic2[dataset]+'.pth'))
    del tmp
    
    _tmp = []
    if count > 1:
        for i in range(1, count):
            _tmp.append(torch.load(os.path.join(save_dir, str(i)+dic2[dataset]+'.pth')))
        _tmp.append(torch.load(os.path.join(save_dir, 'final'+dic2[dataset]+'.pth')))
        res = torch.cat(_tmp).cpu()
        print(dataset, res.shape, 'save in: ', save_dir)
        torch.save(res, os.path.join(save_dir, dic2[dataset]+'.pth'))
        
        # delete  
        for i in range(1, count):
            os.remove(os.path.join(save_dir, str(i)+dic2[dataset]+'.pth'))
        os.remove(os.path.join(save_dir, 'final'+dic2[dataset]+'.pth'))
        