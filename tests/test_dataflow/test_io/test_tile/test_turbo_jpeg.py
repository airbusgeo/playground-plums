import os.path as op

import numpy as np
import cv2

from playground_plums.dataflow.io.tile._vendor.turbojpeg import TurboJPEG, TJPF, TJSAMP


def phash_compare(img1, img2):
    hasher = cv2.img_hash_PHash.create()
    return hasher.compare(hasher.compute(img1), hasher.compute(img2))


def test_turbo():
    img = np.load(op.join(op.dirname(__file__), '_data', 'mona_lisa.npy'))
    turbo = TurboJPEG()

    encoded = turbo.encode(img, quality=95, pixel_format=TJPF.BGR, jpeg_subsample=TJSAMP.YUV420)
    assert img.size > len(encoded)
    assert encoded == turbo.encode(img, quality=95, pixel_format=TJPF.BGR, jpeg_subsample=TJSAMP.YUV420)
    assert turbo.info(encoded) == (341, 229, 'YUV420', 'BGR')

    decoded = turbo.decode(encoded)
    np.testing.assert_equal(decoded, turbo.decode(encoded))
    assert not np.array_equal(decoded, turbo.decode(encoded, fast_dct=True, fast_upsample=False))
    assert not np.array_equal(decoded, turbo.decode(encoded, fast_dct=False, fast_upsample=True))
    assert not np.array_equal(decoded, turbo.decode(encoded, fast_dct=True, fast_upsample=True))
    assert phash_compare(img, decoded) <= 5
