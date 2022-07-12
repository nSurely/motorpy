class Mutable:

    def _update(self, persist: bool = False, **kwargs) -> None:
        """
        Update a field on the model, call update to persist changes in the API.
        This tracks what has changed and only updates the API if something has changed or is set.

        Args:
            persist (bool): whether to persist the changes to the API. Defaults to False.
            **kwargs: the model fields to update.

        Note: when doing multiple updates, it is recommended to call update() after all updates are made.
        """
        if not kwargs:
            return
        for key, value in kwargs.items():
            object.__setattr__(self, key, value)
            self.__fields_set__.add(key)