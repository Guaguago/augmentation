GPUID=0
CONSTR_W=n2
RHO_W=2
CONSTR_C=n3
RHO_C=1
RATIO=1
PERC=$(python -c "print(int($RATIO*100))")
SEED=1
python3 -u train.py --gpuid $GPUID \
--dir /apdcephfs/private_chencxu/taiji_inputs/augmentation/data/snli_1.0/ \
--train_res train.content_word.json,train.all_rel.json \
--val_res dev.content_word.json,dev.all_rel.json \
--within_constr ${CONSTR_W} --rho_w ${RHO_W} --cross_constr ${CONSTR_C} --rho_c ${RHO_C} --constr_on 1,2,3 \
--encoder rnn --rnn_type lstm --dropout 0.2 --epochs 100 --learning_rate 0.0001 --clip 5 \
--percent ${RATIO} --seed ${SEED} \
--save_file /apdcephfs/private_chencxu/taiji_outputs/augmentation/models/${CONSTR_W//,}_rho${RHO_W}_${CONSTR_C//,}_rho${RHO_C//.}_bilstm_lr00001_perc${PERC}_seed${SEED} \
 | tee /apdcephfs/private_chencxu/taiji_outputs/augmentation/models/${CONSTR_W//,}_rho${RHO_W}_${CONSTR_C//,}_rho${RHO_C//.}_bilstm_lr00001_perc${PERC}_seed${SEED}.txt \
 > /apdcephfs/private_chencxu/taiji_outputs/augmentation/train_aug.log