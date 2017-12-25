class LiquifySimple(object):
    id = 12
    miles = "davis"
    john = "coltrane"

    __liquify__ = ["miles", "john"]


class LiquifyComplex(LiquifySimple):
    __liquify__ = dict(
        attributes=["miles", "john"],
        group="complex"
    )

class LiquifyNested(LiquifySimple):
    miles = LiquifySimple()
