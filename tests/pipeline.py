import numpy as np
import stim

from highwater import circuits, decode


def test_dem_decomposes():
    """Every error splits into components of at most two detectors."""
    dem = circuits.model(circuits.build(circuits.Params(d=3, p=1e-3, rounds=3)))
    for inst in dem.flattened():
        if not isinstance(inst, stim.DemInstruction) or inst.type != "error":
            continue
        detectors = 0
        for target in inst.targets_copy():
            if not isinstance(target, stim.DemTarget):
                continue
            if target.is_separator():
                detectors = 0
            elif target.is_relative_detector_id():
                detectors += 1
                assert detectors <= 2


def test_decoder_beats_trivial():
    """MWPM beats predicting no logical flip at all.

    This is the check that fails when the pipeline runs end to end and still
    produces plausible-looking garbage: a decoder wired up but not decoding.
    """
    circuit = circuits.build(circuits.Params(d=3, p=3e-3, rounds=3))
    detectors, observables = circuits.sample(circuit, shots=10_000, seed=1)
    predicted = decode.matcher(circuits.model(circuit)).decode_batch(detectors)

    mwpm = np.count_nonzero(np.any(predicted != observables, axis=1))
    trivial = np.count_nonzero(np.any(observables, axis=1))
    assert mwpm < trivial / 2


def test_one_shot_matches_batch():
    """decode() and decode_batch() agree shot by shot.

    The latency path uses the first and the accuracy path the second, so the
    two curves describe the same decoder only while this holds.
    """
    circuit = circuits.build(circuits.Params(d=5, p=3e-3, rounds=5))
    detectors, _ = circuits.sample(circuit, shots=64, seed=2)
    matching = decode.matcher(circuits.model(circuit))
    batch = matching.decode_batch(detectors)
    for shot, row in zip(detectors, batch, strict=True):
        prediction = matching.decode(shot)
        assert isinstance(prediction, np.ndarray)
        assert np.array_equal(prediction, row)
