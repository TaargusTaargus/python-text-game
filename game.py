import json
from interpreter import standard_format_parser
from sys import argv, exit

## variables
DEBUG = 1   

## constants
VIEW_ROOM_OBJECTS_VERB = 'objects'
VIEW_OBJECT_EVENTS_VERB = 'actions'

## testing
INIT_ROOM = 'lounge'

state = {
    'command': None,
    'object': None,
    'room': None
}

game = { 
    'config' : None,
    'game' : standard_format_parser( argv[ 1 ] ),
    'state': state
}

while True:
   
    try:
        command = input( 'What do you want to do: ' )
        command = command.strip()

        if command == 'exit':
            print( 'Exiting game.' )
            exit( 0 )

        command = command.split( ' ' )
        command = {
            'verb': command[ 0 ],
            'object': ' '.join( command[ 1 : ] )
        }
        
        state[ 'command' ] = command
        state[ 'room' ] = game[ 'game' ][ 'rooms' ][ INIT_ROOM ]
        
        ## check for special object command
        if command[ 'verb' ] == VIEW_ROOM_OBJECTS_VERB:
            print( f"The room has the following object(s): {', '.join( list( state[ 'room' ][ 'objects' ].keys() ) )}." )
            continue
        
        ## if we can't find the object or recognize it, then we pretend the room is the object
        try:
            state[ 'object' ] = game[ 'game' ][ 'rooms' ][ INIT_ROOM ][ 'objects' ][ command[ 'object' ] ]
        except KeyError as e:
            state[ 'object' ] = state[ 'room' ]
   
        ## check for special action command
        if command[ 'verb' ] == VIEW_OBJECT_EVENTS_VERB:
            print( f"The object has the following potential action(s): {', '.join( list( state[ 'object' ][ 'events' ].keys() ) )}." )
            continue
                  
        ## now we try to trigger the event
        try:
            print( state[ 'object' ][ 'events' ][ command[ 'verb' ] ] )
        except KeyError as e:
            print( f"You can't do that to the {state[ 'object' ]}." )
                  
                  
        if DEBUG > 0:
            print( f'''
                object: {command[ 'object' ] }
                verb: {command[ 'verb' ]}
            ''' )
            
    except KeyboardInterrupt as e:
        print( "Exiting game." )
        exit( 0 )
