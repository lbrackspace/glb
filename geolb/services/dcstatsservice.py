from geolb.services.base import BaseService
from geolb.models.persistence import glb, node, monitor, region, dcstats


class DCStatsService(BaseService):
    def get_all(self):
        #Will be heavy, needs pagination if this call is needed.
        stats = self.dcstatspersistence.dsp.get_all()
        return stats

    def create(self, stats_json):
        #Logical validation and other operations
        #Call other services to do validation of child objects or do
        #All validation for 'one' call in the same place..

        dc_stats = []
        if stats_json is not None:
            for s in stats_json:
                dc_stats.append(dcstats.DCStatModel(
                    location=s.get('location'), status=s.get('status'),
                    glb_id=s.get('glb_id'), response=s.get('response')))

        dc_stats = self.dcstatspersistence.dsp.create(dc_stats)
        return dc_stats

    def update(self, stats_json):
        #Batch update..., heavy
        if stats_json is not None:
            for s in stats_json:
                g_id = s.get('glb_id')
                location = s.get('location')
                response = s.get('response')

                #glb operations currently ignores account_id, should have an
                # 'admin' get by id and other admin type calls
                g = self.glbpersistence.gp.get(1, g_id)
                g.update_type = 'NONE'
                #cstat = self.dcstatspersistence.dsp.get(s.get('glb_id'),
                #                                        s.get('location'))
                for ds in g.dc_stats:
                    if location in ds.location:
                        ds.location = s.get('location')
                        ds.status = s.get('status')
                        ds.response = s.get('response')

                        #should probably do this elsewhere,
                        # get data elsehow/differently,
                        # also need to check for errors etc..

                if 'ERROR' in g.dc_stats:
                    g.status = 'ERROR'
                else:
                    if not 'OFFLINE' in g.dc_stats:
                        g.status = 'ACTIVE'

                self.glbpersistence.gp.update(1, g_id, g)
            #What to return?
        return True


class DCStatsServiceOps(object):
    def __init__(self):
        self.ds = DCStatsService()