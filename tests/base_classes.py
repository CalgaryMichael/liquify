class Base(object):
    _private = "You found me!"

    def __init__(self, id=12, miles="davis", john="coltrane", **kwargs):
        self.id = id
        self.miles = miles
        self.john = john
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __str__(self):
        return "miles {}".format(self.miles)

    @property
    def artists(self):
        return [self.miles, self.john]

    def jazz(self):
        return "Birth of Cool (1957)"


class LiquifySimple(Base):
    __liquify__ = ["miles", "john"]


class LiquifyComplex(Base):
    __liquify__ = dict(
        attributes=["miles", "john"],
        group="complex"
    )


class LiquifyNested(LiquifySimple):
    def __init__(self, id=12, miles=LiquifySimple(), john="coltrane", **kwargs):
        super(LiquifyNested, self).__init__(
            id=id, miles=miles, john=john, **kwargs
        )

    def nested(self):
        return LiquifySimple()
