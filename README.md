Yet another AlphaZero program, applied to chess (school project, 2018).

Iterative implementation using Keras.

## Usage

Clone project
```bash
git clone https://github.com/swasun/Yet-Another-AlphaZero
cd Yet-Another-AlphaZero/yaaz/src
```

Run the self play module to generate new entries in the dataset.
```bash
python3 self_play.py
```

Run the optimisation module to train the network using the dataset.
```bash
python3 optimisation.py
```

Run the evaluator module to evaluate the best module.
```bash
python3 evaluator.py
```

## Dependencies

* python3
* numpy
* keras using a GPU backend (for example: tensorflow-gpu)
* python-chess (https://pypi.org/project/python-chess/)
* A GPU compatible with CUDA

## References

[1] Silver, D., Schrittwieser, J., Simonyan, K., Antonoglou, I., Huang, A., Guez, A., Hubert, T., Baker, L., Lai, M., Bolton, A., Chen, Y., Lillicrap, T., Hui, F., Sifre, L., van den Driessche, G., Graepel, T. & Hassabis, D. (2017). Mastering the game of Go without human knowledge. Nature, 550, 354--.

[2] Silver, David, Huang, Aja, Maddison, Chris J., Guez, Arthur, Sifre, Laurent, van den Driessche, George, Schrittwieser, Julian, Antonoglou, Ioannis, Panneershelvam, Veda, Lanctot, Marc, Dieleman, Sander, Grewe, Dominik, Nham, John, Kalchbrenner, Nal, Sutskever, Ilya, Lillicrap, Timothy, Leach, Madeleine, Ka-00vukcuoglu, Koray, Graepel, Thore and Hassabis, Demis. "Mastering the Game of Go with Deep Neural Networks and Tree Search." Nature 529 , no. 7587 (2016): 484--489.

[3] Silver, David, Thomas Hubert, Julian Schrittwieser, Ioannis Antonoglou, Matthew Lai, Arthur Guez, Marc Lanctot, Laurent Sifre, Dharshan Kumaran, Thore Graepel, Timothy P. Lillicrap, Karen Simonyan and Demis Hassabis. “Mastering Chess and Shogi by Self-Play with a General Reinforcement Learning Algorithm.” CoRR abs/1712.01815 (2017): n. pag.

[4] C. B. Browne et al., "A Survey of Monte Carlo Tree Search Methods," in IEEE Transactions on Computational Intelligence and AI in Games, vol. 4, no. 1, pp. 1-43, March 2012. doi: 
10.1109/TCIAIG.2012.2186810
[5] A general reinforcement learning algorithm that masters chess, shogi, and Go through self-play, D Silver, T Hubert, J Schrittwieser, I Antonoglou, M Lai, A Guez, M Lanctot, L Sifre, D Kumaran, T Graepel, T Lillicrap, K Simonyan, D Hassabis, December 20181
