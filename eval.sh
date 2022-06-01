DEVICE=0

python3 -u eval.py \
--gpuid ${DEVICE} \
--dir /apdcephfs/private_chencxu/taiji_inputs/augmentation/data/snli_1.0/ \
--data snli-test.hdf5 \
--word_vecs glove.hdf5 \
--encoder rnn --rnn_type lstm --attention local --classifier local --dropout 0.0 \
--load_file /apdcephfs/private_chencxu/taiji_outputs/augmentation/models/lstm_clip5_adam_lr00001 | tee /apdcephfs/private_chencxu/taiji_outputs/augmentation/models/lstm_clip5_adam_lr00001.evallog.txt \
> /apdcephfs/private_chencxu/taiji_outputs/augmentation/eval.log