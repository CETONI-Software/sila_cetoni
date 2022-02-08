from qmixsdk import qmixpump
from sila2.framework.command.parameter import Parameter
from sila2.framework.errors.validation_error import ValidationError


def evaluate_units(parameter: Parameter, requested_volume_unit, requested_time_unit=None):
    """
    Converts the given volume and time unit from strings to qmixpump units
    and returns a 2-tuple or a 3-tuple (if a time unit is provided).
        :param parameter: the parameter that needs the conversion
        :param requested_volume_unit: the volume unit to convert to a string
        :param requested_time_unit: the time unit to convert to a string
    """
    prefix_string = requested_volume_unit[0] if len(requested_volume_unit) > 1 else " "
    volume_unit_string = requested_volume_unit[-1]

    prefix = evaluate_prefix(prefix_string, parameter)
    volume_unit = evaluate_volume_unit(volume_unit_string, parameter)

    if requested_time_unit:
        time_unit = evaluate_time_unit(requested_time_unit, parameter)
        return (prefix, volume_unit, time_unit)

    return (prefix, volume_unit)


def evaluate_prefix(prefix_string, parameter: Parameter):
    """
    Converts the given prefix_string to a `qmixpump.UnitPrefix`
    :param prefix_string: The string to convert
    :param parameter: The command parameter that is currently converted
                      (just for error-description purposes)
    """
    switcher = {
        " ": qmixpump.UnitPrefix.unit,
        "d": qmixpump.UnitPrefix.deci,
        "c": qmixpump.UnitPrefix.centi,
        "m": qmixpump.UnitPrefix.milli,
        "u": qmixpump.UnitPrefix.micro,
        "µ": qmixpump.UnitPrefix.micro,
    }
    prefix = switcher.get(prefix_string)
    if not prefix:
        raise ValidationError(parameter, f"Wrong prefix: '{prefix_string}' not supported")

    return prefix


def evaluate_volume_unit(volume_unit_string, parameter: Parameter):
    """
    Converts a given volume_unit_string to a `qmixpump.VolumeUnit`
    :param volume_unit_string: The string to convert
    :param parameter: The command parameter that is currently converted
                      (just for error-description purposes)
    """
    if volume_unit_string == "l":
        return qmixpump.VolumeUnit.litres

    raise ValidationError(parameter, f"Wrong volume unit: '{volume_unit_string}' not supported")


def evaluate_time_unit(time_unit_string, parameter: Parameter):
    """
    Converts a given time_unit_string into a `qmixpump.TimeUnit`
    :param time_unit_string: The string to convert
    :param parameter: The command parameter that is currently converted
                      (just for error-description purposes)
    """
    switcher = {"s": qmixpump.TimeUnit.per_second, "min": qmixpump.TimeUnit.per_minute, "h": qmixpump.TimeUnit.per_hour}

    time_unit = switcher.get(time_unit_string)
    if not time_unit:
        raise ValidationError(parameter, f"Wrong time_unit: '{time_unit_string}' not supported")

    return time_unit


def volume_unit_to_string(qmix_volume_unit) -> str:
    """
    Converts a volume unit given as a named tuple to a string
        :param qmix_volume_unit: a named tuple consisting of a prefix and a volume_unit
    """
    prefix, volume_unit = qmix_volume_unit
    prefix_string = prefix_to_string(prefix)
    volume_unit_string = "l"

    return f"{prefix_string}{volume_unit_string}"


def flow_unit_to_string(flow_unit) -> str:
    """
    Converts a flow unit given as a named tuple to a string
        :param flow_unit: a named tuple consisting of a prefix, a volume_unit and a time_unit
    """
    prefix, volume_unit, time_unit = flow_unit
    prefix_string = prefix_to_string(prefix)
    volume_unit_string = "l"
    time_unit_string = time_unit_to_string(time_unit)
    return f"{prefix_string}{volume_unit_string}/{time_unit_string}"


def flow_unit_to_tuple(flow_unit) -> tuple:
    """
    Converts a flow unit given as a named tuple to a string
        :param flow_unit: a named tuple consisting of a prefix, a volume_unit and a time_unit
    """
    prefix, volume_unit, time_unit = flow_unit
    prefix_string = prefix_to_string(prefix)
    volume_unit_string = "l"
    time_unit_string = time_unit_to_string(time_unit)
    return (prefix_string + volume_unit_string, time_unit_string)


def prefix_to_string(prefix):
    """
    Converts a given prefix to a human readable string
        :param prefix: qmixpump.UnitPrefix
    """
    switcher = {
        qmixpump.UnitPrefix.deci: "d",
        qmixpump.UnitPrefix.centi: "c",
        qmixpump.UnitPrefix.milli: "m",
        qmixpump.UnitPrefix.micro: "µ",
    }  # default = no prefix
    return switcher.get(prefix, "")


def time_unit_to_string(time_unit):
    """
    Converts a given time_unit to a human readable string
        :param time_unit: qmixpump.TimeUnit
    """
    switcher = {qmixpump.TimeUnit.per_hour: "h", qmixpump.TimeUnit.per_minute: "min"}  # default = "per_second"
    return switcher.get(time_unit, "s")
