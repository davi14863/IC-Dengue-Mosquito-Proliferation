import numpy as np
import rasterio
import os

from split_merge.split_merge_image import SplitMergeImage



def extract_img_geotrans_Tiff(filepath_tiff):
    with rasterio.open(filepath_tiff) as src:
        band_b = src.read(1)  # Banda 1: Vermelho
        band_g = src.read(2)  # Banda 2: Verde
        band_r = src.read(3)  # Banda 3: Azul
        rgb_image = np.dstack((band_r, band_g, band_b))  # Matriz [height, width, 3]
        
        return rgb_image


def list_tif_images(img_dir_path):
    list_tif_paths = []

    if not os.path.isdir(img_dir_path):
        print(f"O diretório {img_dir_path} não existe.")
        return []
    
    for file in os.listdir(img_dir_path):
        full_path_temp = os.path.join(img_dir_path, file)
        if os.path.isfile(full_path_temp) and file.lower().endswith('.tif'): # Verifica se é um arquivo .tif
            list_tif_paths.append(full_path_temp)
    
    return list_tif_paths




list_tif_paths = list_tif_images('./tif_images')
split_merge = SplitMergeImage()
len_block_side = 2048 
blocks_img_path = './blocks_images'


for tif_path in list_tif_paths:
    print(f"Lendo imagem tif: {tif_path}")
    rgb_image = extract_img_geotrans_Tiff(tif_path)
    print(f"\t...imagem tif lida.")

    tif_img_name = os.path.basename(tif_path)
    tif_img_name, _ = os.path.splitext(tif_img_name)
    

    n_blocks = split_merge.split_image(rgb_image, len_block_side)

    split_merge.save_blocks(blocks_img_path, tif_img_name)





    