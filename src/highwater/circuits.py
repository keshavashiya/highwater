"""The rotated surface-code memory experiment and its detector error model.

The circuit is Stim's own generated experiment, not a hand-built one. A single
error rate p sets all four noise channels: uniform circuit-level depolarising
noise. Only the Z basis is run. Every number this repository produces depends
on those three choices.
"""

from dataclasses import dataclass

import stim


@dataclass(frozen=True)
class Params:
    """One experiment: code distance d, physical error rate p, and rounds.

    rounds is always stated. The convention throughout is rounds = d, the
    standard one for a memory experiment.
    """

    d: int
    p: float
    rounds: int


def build(params: Params) -> stim.Circuit:
    """The noisy memory circuit for one experiment."""
    p = params.p
    return stim.Circuit.generated(
        "surface_code:rotated_memory_z",
        distance=params.d,
        rounds=params.rounds,
        after_clifford_depolarization=p,
        before_measure_flip_probability=p,
        after_reset_flip_probability=p,
        before_round_data_depolarization=p,
    )


def model(circuit: stim.Circuit) -> stim.DetectorErrorModel:
    """The detector error model a matching decoder can be built from."""
    # decompose_errors=True is required. Without it the model keeps hyperedges,
    # errors that flip three or more detectors, which a matching decoder cannot
    # match on, and the failure is quiet.
    return circuit.detector_error_model(decompose_errors=True)


def sample(circuit: stim.Circuit, shots: int, seed: int):
    """Detector samples and the true observable flips, one row per shot."""
    sampler = circuit.compile_detector_sampler(seed=seed)
    return sampler.sample(shots, separate_observables=True)
