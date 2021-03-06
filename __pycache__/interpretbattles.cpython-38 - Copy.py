U
    N2^�  �                   @   s4   d dl Z d dlZd dlZdd� Zd dlZdd� ZdS )�    Nc                  G   s   t dd� t| � D ��S )Nc                 s   s   | ]}t �tj|�V  qd S �N)�	functools�reduce�operator�mul)�.0�data� r	   �AC:\Users\Adam\PycharmProjects\ClashRoyaleMeta\interpretbattles.py�	<genexpr>   s     zsumproduct.<locals>.<genexpr>)�sum�zip)�listsr	   r	   r
   �
sumproduct   s    r   c                    sr  t �d�}t|||�D �]L��| ����fdd�| D �}ttdd� |D ������ttdd� |D ���� ttdd� �D �����fdd�tt���D ��d	gt�� ��D ]�z:t�fd
d�|D ��t�fdd�|D �� �����< W n   d	�����< Y nX �D ]�� z`t� �fdd�|D ��t� �fdd�|D ��t� �fdd�|D ��  ����� ��� �< W n$   d����� ��� �< Y nX �qq���fdd�tt���D �}|�dt	�� d t	�� �}|�
dd� |�ddi�}	t��d }
|�|
d dd|	� |�|
d dd|	� tt���D ]�}t�| �d	k�r�|�d	|d �| |	� |�|d d	�| |	� |�|
| d	�| |	� n<|�d	|d d|	� |�|d d	d|	� |�|
| d	d|	� tt���D ]$}|�|d |d �| | � �q�|�|
| d�| � |�|
| d|| � �q0|�|
d|
t�� ddt|�dd�� tt|���� q|��  d S )Nz	demo.xlsxc                    s<   g | ]4}|d  �kr|d  � kr|d � � �� � kr|�qS )�   �   )�lower�r   �i)�maxT�minT�typer	   r
   �
<listcomp>   s
        z%battleDeckPrinter.<locals>.<listcomp>c                 s   s   | ]}|d  d V  qdS )�   r   Nr	   �r   �_r	   r	   r
   r      s     z$battleDeckPrinter.<locals>.<genexpr>c                 s   s   | ]}|d  d V  qdS )�   r   Nr	   r   r	   r	   r
   r      s     c                 s   s   | ]
}|V  qd S r   r	   r   r	   r	   r
   r      s     c                    s   g | ]}d gt � � �qS )�      �?)�lenr   )�lArchetypesr	   r
   r      s     r   c                    s    g | ]}|d  d � kr|�qS )r   r   r	   r   ��
archwinnerr	   r
   r      s      c                    s    g | ]}|d  d � kr|�qS )r   r   r	   r   r    r	   r
   r      s      c                    s0   g | ](}|d  d �kr|d d � kr|�qS )r   r   r   r	   r   ��	archloserr!   r	   r
   r      s       c                    s0   g | ](}|d  d �kr|d d � kr|�qS )r   r   r   r	   r   r"   r	   r
   r      s       r   c                    s   g | ]}t � �| ��qS r	   )r   r   )�lArchPrevalence�	lWinTabler	   r
   r   "   s     �T�-zA:A�   �boldTr   r   Z
Prevalence�   z
Meta ScoreZMiscZ3_color_scalez#FFFFFF)r   Z	mid_valueZ	mid_color)�
xlsxwriterZWorkbook�range�list�set�extendr   �indexZadd_worksheet�strZ
set_columnZ
add_format�writeZconditional_format�print�close)ZlOriginalBattlesr   ZbottomTZtopTZ
trophystep�wb�lBattlesZ
lViability�wsr)   Z	rowoffsetr   �jr	   )r#   r!   r$   r   r%   r   r   r   r
   �battleDeckPrinter	   sX    
:`$"�r9   )r   r   r+   r   �csvr9   r	   r	   r	   r
   �<module>   s
   