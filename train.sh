DEVICE=0

python3 -u train.py --gpuid ${DEVICE} \
--dir /apdcephfs/private_chencxu/taiji_inputs/augmentation/data/snli_1.0/ \
--train_data snli-train.hdf5 --val_data snli-val.hdf5 --word_vecs glove.hdf5 \
--encoder rnn --rnn_type lstm  --attention local --classifier local --dropout 0.2 --epochs 100 --learning_rate 0.0001 --clip 5 \
--save_file /apdcephfs/private_chencxu/taiji_outputs/augmentation/models/lstm_clip5_adam_lr00001 \
| tee /apdcephfs/private_chencxu/taiji_outputs/augmentation/models/lstm_clip5_adam_lr00001.txt \
> /apdcephfs/private_chencxu/taiji_outputs/augmentation/train.log