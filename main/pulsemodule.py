import pulsectl
import time

with pulsectl.Pulse('volume-increaser') as pulse:
    timebegin=time.time()    
    while True:
        if time.time()-timebegin>5:
            print("Time out!")
            break
        # Get the list of sink inputs
        sink_inputs = pulse.sink_input_list()

        # Iterate over the sink inputs
        for sink_input in sink_inputs:
        # Check if the sink input is connected to a Bluetooth device
            if 'blue' in sink_input.name or any('blue' in str(item) for item in sink_input.proplist.items()):
                # Create a null sink
                # Check if the sink 'blue_sink' already exists
                existing_sinks = pulse.sink_list()
                if not any(sink_name == f'blue_sink{sink_input.index}' for sink_name in [sink.name for sink in existing_sinks]):
                    # Load the null sink module with the specified sink name and properties
                    pulse.module_load('module-null-sink', f"sink_name='blue_sink{sink_input.index}' format='s16le' rate='44100' channels='2'")
                
                # Get the index of the blue_sink
                blue_sink = pulse.get_sink_by_name(f'blue_sink{sink_input.index}')
                # Move the sink input to the null sink
                
                pulse.sink_input_move(sink_input.index, blue_sink.index)
                blue_source = pulse.get_source_by_name(f'blue_sink{sink_input.index}.monitor')

                pulse.source_default_set(blue_source)
                break
        time.sleep(0.2)