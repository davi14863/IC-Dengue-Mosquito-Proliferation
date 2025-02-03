import numpy as np
import cv2
import os  

class SplitMergeImage:
    """
    Classe para dividir uma imagem em blocos e reconstruí-la após processamento.

    :param image: A imagem original.
    :type image: numpy.ndarray
    :param block_size: O tamanho de lado dos blocos quadrados.
    :type block_size: int
    :param blocks: Lista de blocos particionados.
    :type blocks: list
    :param offsets: Lista de offsets (deslocamentos) dos blocos na imagem original.
    :type offsets: list
    :param original_shape: Dimensões originais da imagem.
    :type original_shape: tuple
    :param processed_blocks: Lista de blocos processados.
    type processed_blocks: list
    """
    def __init__(self):
        """Inicializa a classe com atributos padrão."""
        self.image = None
        self.block_size = None
        self.blocks = []
        self.offsets = []
        self.original_shape = None
        self.processed_blocks = []

    def split_image(self, image: np.ndarray, block_size: int) -> int:
        """
        Divide uma imagem em blocos de tamanho especificado.

        :param image: A imagem a ser particionada.
        :param block_size: O tamanho dos blocos quadrados.

        :return blocks: Lista de blocos particionados.
        """

        self.image = image
        self.block_size = block_size
        self.original_shape = image.shape
        self.blocks = []
        self.offsets = []  # Resetar os offsets


        h, w, _ = image.shape

        for i in range(0, h, block_size):
            for j in range(0, w, block_size):
                block = image[i:i + block_size, j:j + block_size]
                if block.shape[0] < block_size or block.shape[1] < block_size:
                    block = cv2.copyMakeBorder(block, 0, block_size - block.shape[0], 0, block_size - block.shape[1], cv2.BORDER_CONSTANT, value=[255, 255, 255])
                if block.shape[0] == block_size and block.shape[1] == block_size:
                    self.blocks.append(block)
                    self.offsets.append((i, j))
        return len(self.blocks)

    def save_blocks(self, path_blocks_img: str, img_name: str):
        i=0
        for block, offset in zip(self.blocks, self.offsets):
            if not cv2.imwrite(os.path.join(path_blocks_img,img_name+'_block'+str(i).zfill(5)+'.jpg'), block):
                print(f"ERRO ao salvar o bloco de imagem {img_name}_block{str(i).zfill(5)}.jpg")
            try:
                with open(os.path.join(path_blocks_img,img_name+'_offset_block'+str(i).zfill(5)+'.txt'), 'w') as f:
                    f.write(str(offset))  # Escreve a tupla como string
            except IOError as e:
                print(f"Erro ao tentar salvar o arquivo: {e}")
            i=i+1

    
    def merge_image(self, processed_blocks: list) -> np.ndarray:
        """
        Reconstrói a imagem a partir dos blocos processados.

        :param processed_blocks: Lista de blocos processados.
        :return merged_image: Imagem reconstituída.
        """
        h, w, _ = self.original_shape
        merged_image = np.zeros(self.original_shape, dtype=np.uint8)

        block_size = self.block_size
        idx = 0

        for i in range(0, h, block_size):
            for j in range(0, w, block_size):
                block = processed_blocks[idx]
                if i + block_size > h:
                    block = block[:h - i, :]
                if j + block_size > w:
                    block = block[:, :w - j]
                merged_image[i:i + block.shape[0], j:j + block.shape[1]] = block
                idx += 1
        
        return merged_image
