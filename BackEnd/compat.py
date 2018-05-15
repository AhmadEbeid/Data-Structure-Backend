try:
    from django.contrib.postgres import fields as postgres_fields
    from psycopg2.extras import DateRange, DateTimeTZRange, NumericRange
except ImportError:
    postgres_fields = DateRange = DateTimeTZRange = NumericRange = None