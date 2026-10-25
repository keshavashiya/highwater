"""PyMatching's sparse-blossom MWPM decoder, built once from a detector error model.

No timing and no statistics here. Both doors into the decoder are PyMatching's
own methods on the object this returns: decode() for one shot, decode_batch()
for many. They are not wrapped, because the latency path times decode()
directly and a wrapper would add its own call overhead to every timed decode.
"""

import pymatching
import stim


def matcher(dem: stim.DetectorErrorModel) -> pymatching.Matching:
    """Build the decoder. This is graph construction, not decoding."""
    return pymatching.Matching.from_detector_error_model(dem)
