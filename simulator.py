"""
TODO: add a current real & virtual time and weight
"""
import re
import copy

"""Simple class for packet
"""
class Packet (object):
    """Simple class for packet"""
    def __init__(self):
        self.flow_id = None
        self.size = None
        self.rsize = None

        # arrival time
        self.arrival_time = None

        # real time
        self.r_start_time = None
        self.r_finish_time = None

        # GPS virtual time
        self.v_start_time = None
        self.v_finish_time = None

   
def empty(obj):
    return len(obj) == 0


class GPSSim(object):
    """TODO"""
    def __init__(self):
        self.flows = {}
        self.packets = []
        self.flow_weights = {}
        self.events = {
            "finished": [],
            "future": [],
            "queued": []
        }
        # initialize all time instances
        self.current_v_time = 0
        self.current_r_time = 0
        self.current_weight = 0

        self.pre_v_time = 0
        self.pre_r_time = 0
        self.pre_weight = 0

    def read_pkt_from_file(self, filename):

        flow_index = 1
        with open(filename, 'r') as fp:
            for line in fp:
                if line.startswith("#") or (len(line.strip()) == 0):
                    # comments or empty line, ignore
                    pass
                else:
                    try:
                        s = line.split(":")
                        if len(s) == 1:
                            self.flow_weights[flow_index] = 1
                            s = s[0]
                        else:
                            self.flow_weights[flow_index] = int(s[0].strip())
                            s = s[1]

                        for pkt_info in s.split(","):
                            pkt_segs = re.split("\s+", pkt_info.strip())
                            arrival_time = int(pkt_segs[0])
                            length = int(pkt_segs[1])
                            pkt = Packet()
                            pkt.arrival_time = arrival_time
                            pkt.size = length
                            pkt.rsize = length
                            pkt.r_start_time = arrival_time
                            pkt.flow_id = flow_index
                            self.packets.append(copy.deepcopy(pkt))

                        self.flows[flow_index] = []

                        flow_index += 1
                    except:
                        print("Input format is not correct")
                        exit(1)
        self.packets.sort(key=lambda x: x.arrival_time)
        for pkt in self.packets:
            self.events["future"].append(pkt)

    def run(self):
        """Simulate GPS

        Note that,
        1. self.events["future"] corresponds to arrivals, which are sorted by
        real arrival time!!!!
        2. self.events["queued"] corresponds to "departures", which are sorted by
        virtual finish time!!!!
        3. self.events["finished"] stores all packets that finished their service
        (i.e., already departure)

        """

        # there are "arrivals" or "departure" or both to handle
        while not (empty(self.events["future"]) and empty(self.events["queued"])):

            # packet arrival
            if not empty(self.events["future"]):

                pkt = self.events["future"][0]
                # add to respective flow

                self.flows[pkt.flow_id].append(pkt)
                self.current_r_time = pkt.arrival_time

                try:
                    self.current_v_time = self.pre_r_time + (self.current_r_time - self.pre_r_time) / self.pre_weight
                except ZeroDivisionError:
                    self.current_v_time = self.pre_v_time

                # Departing all packets that should depart    
                while (not empty(self.events["queued"])) and (self.events["queued"][0].v_finish_time <= self.current_v_time):
                    self._departure_handler()

                # Move current packet to "queue"
                if len(self.flows[pkt.flow_id]) > 1 and self.flows[pkt.flow_id][-2].v_finish_time > self.current_v_time:
                    # this packet arrives before the previous one (in the same
                    # flow)'s departure
                    pkt.v_start_time = self.flows[pkt.flow_id][-2].v_finish_time
                else:
                    # this packet arrives after
                    pkt.v_start_time = self.current_v_time
                    # Update current total weight
                    self.current_weight = self.pre_weight + self.flow_weights[pkt.flow_id]
                    self._update_queued_packets(self.pre_weight, self.current_v_time - self.pre_v_time,
                                                self.current_weight)

                pkt.v_finish_time = pkt.v_start_time + pkt.size / self.flow_weights[pkt.flow_id]
                # queued this packet
                self._enqueue(pkt)
                del self.events["future"][0]

                self.pre_weight = self.current_weight
                self.pre_v_time = self.current_v_time
                self.pre_r_time = self.current_r_time
            else:
                # no arrivals again
                while (not empty(self.events["queued"])):
                    self._departure_handler()

    def _enqueue(self, pkt):
        insert_pos = len(self.events["queued"])
        for i, q_pkt in enumerate(self.events["queued"]):
            if q_pkt.v_finish_time > pkt.v_finish_time:
                insert_pos = i
                break
        self.events["queued"].insert(insert_pos, pkt)

    def _update_queued_packets(self, old_pre_weight, v_timedelta, pre_v_time):
        # Update all queued packets
        for q_pkt in self.events["queued"]:
            # update remaining size
            if q_pkt.v_start_time < pre_v_time:
                q_pkt.rsize -= (self.flow_weights[q_pkt.flow_id] / old_pre_weight) * v_timedelta
            # (Not necessary ??)
            # q_pkt.r_finish_time = pre_r_time + q_pkt.rsize / (self.flow_weights[q_pkt.flow_id] / pre_weight)

    def _departure_handler(self):
        pkt = self.events["queued"][0]
        
        v_timedelta = pkt.v_finish_time - self.pre_v_time
        old_pre_weight = self.pre_weight
        self.pre_r_time += v_timedelta * self.pre_weight
        self.pre_v_time = pkt.v_finish_time

        # fill its real finish time
        pkt.r_finish_time = self.pre_r_time

        if self.flows[pkt.flow_id][-1] != pkt:
            pass
            # Unnecessary ??
            #     # next packet arrives before my departure
            #     self.flows[pkt.flow_id][-1].r_start_time = pkt.r_finish_time
            #     self.flows[pkt.flow_id][-1].v_start_time = pkt.v_finish_time
            #     self.flows[pkt.flow_id][-1].v_finish_time = pkt.v_finish_time + self.flows[pkt.flow_id][-1].size / self.flow_weights[pkt.flow_id]
        else:
            self.pre_weight -= self.flow_weights[pkt.flow_id]

        self.events["finished"].append(pkt)
        del self.events["queued"][0]

        # update all queued packets
        self._update_queued_packets(old_pre_weight, v_timedelta, self.pre_v_time)

        # update current virtual time
        try:
            self.current_v_time = self.pre_v_time + (self.current_r_time - self.pre_r_time) / self.pre_weight
        except ZeroDivisionError:
            self.current_v_time = self.pre_v_time


if __name__ == "__main__":
    # Test reading
    gps = GPSSim()
    gps.read_pkt_from_file("packets.txt")

    for pkt in gps.packets:
        print(pkt.flow_id, pkt.arrival_time, pkt.size)

    gps.run()

    for pkt in gps.packets:
        print(pkt.flow_id, pkt.arrival_time, pkt.size, pkt.v_start_time, pkt.v_finish_time)





































