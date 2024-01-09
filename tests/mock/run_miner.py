from neurons.miners.m2m_miner import M2MMiner
from mock.mock_network import mocked_network
from neurons.protocol import Translate


def main():
    with mocked_network():
        miner = M2MMiner()

    miner.axon.start()

    synapse = Translate(
                source_texts=["The capital of Poland is Warsaw. The city was founded in the 13th century."],
                source_lang="en",
                target_lang="pl"
            )

    print("Result: ", miner.forward(synapse))

if __name__ == "__main__":
    main()
