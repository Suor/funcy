@monkey(Field)
def get_choices(inherited, self, include_blank=True, blank_choice=[("", "...")]):
    return inherited(self, include_blank, blank_choice)

@monkey(Field)
def get_choices(self, include_blank=True, blank_choice=[("", "...")]):
    return self._no_monkey.get_choices(self, include_blank, blank_choice)

@monkey(Field)
def get_choices(self, include_blank=True, blank_choice=[("", "...")]):
    return self._no_monkey_get_choices(self, include_blank, blank_choice)
