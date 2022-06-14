import sys

sys.path.insert(0, '../')
import torch
from torch import nn
from torch.autograd import Variable
from holder import *
from util import *
from within_layer import *


class LocalAttention(torch.nn.Module):
    def __init__(self, opt, shared):
        super(LocalAttention, self).__init__()

        if opt.within_constr != '':
            self.w_layer = WithinLayer(opt, shared)

        # bookkeeping
        self.opt = opt
        self.shared = shared
        self.dropout = opt.dropout
        self.hidden_size = opt.hidden_size

        # delta
        self.w = nn.Linear(opt.hidden_size, opt.hidden_size, bias=False)
        # self.delta_w = nn.Linear(opt.hidden_size, opt.hidden_size, bias=False)

    def forward(self, sent1, sent2, delta_w):

        # score tensors of size batch_l x sent_l1 x sent_l2
        # self.shared.score1 = sent1.bmm(sent2.transpose(1,2))
        self.shared.score1 = self.w(sent1).bmm(sent2.transpose(1, 2))
        self.shared.score2 = self.shared.score1.transpose(1, 2).contiguous()

        self.unperturbed_score = self.shared.score1

        # attention
        self.shared.att_soft1 = nn.Softmax(2)(self.shared.score1)
        self.shared.att_soft2 = nn.Softmax(2)(self.shared.score2)

        if self.opt.within_constr != '':
            # get constrained scores
            constr_score1, constr_score2 = self.w_layer(self.shared.score1, self.shared.score2,
                                                        self.shared.att_soft1, self.shared.att_soft2)

            # compute constrained attention
            # and bookkeeping
            self.shared.score1 = constr_score1
            self.shared.score2 = constr_score2

            self.perturbed_score = constr_score1

            self.shared.att_soft1 = nn.Softmax(2)(constr_score1)
            self.shared.att_soft2 = nn.Softmax(2)(constr_score2)

            self.shared.imitate_delta_score = sent1.bmm(delta_w).bmm(sent2.transpose(1, 2))
            self.shared.delta_score = self.perturbed_score - self.unperturbed_score

        return [self.shared.att_soft1, self.shared.att_soft2, self.shared.delta_score, self.shared.imitate_delta_score]

    def begin_pass(self):
        pass

    def end_pass(self):
        pass


if __name__ == '__main__':
    from torch.autograd import Variable

    hidden_size = 3

    opt = Holder()
    opt.hidden_size = 3
    opt.dropout = 0.0
    shared = Holder()
    shared.batch_l = 1
    shared.sent_l1 = 5
    shared.sent_l2 = 8
    shared.input1 = Variable(torch.randn(shared.batch_l, shared.sent_l1, opt.hidden_size), True)
    shared.input2 = Variable(torch.randn(shared.batch_l, shared.sent_l2, opt.hidden_size), True)

    # build network
    attender = LocalAttention(opt, shared)

    # update batch info
    shared.batch_l = 1
    shared.sent_l1 = 5
    shared.sent_l2 = 8

    # run network
    rs = attender(shared.input1, shared.input2)
    print(rs)
    print(rs[0].sum(2))
    print(rs[1].sum(2))
