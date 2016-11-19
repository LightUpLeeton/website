import prestans.ext.data.adapters
import prestans.ext.data.adapters.ndb

import lul.models
import lul.rest.models

prestans.ext.data.adapters.registry.register_adapter(
    prestans.ext.data.adapters.ndb.ModelAdapter(
        rest_model_class=lul.rest.models.Location, 
        persistent_model_class=lul.models.POILocation
    )
)

prestans.ext.data.adapters.registry.register_adapter(
    prestans.ext.data.adapters.ndb.ModelAdapter(
        rest_model_class=lul.rest.models.PointOfInterest, 
        persistent_model_class=lul.models.PointOfInterest
    )
)