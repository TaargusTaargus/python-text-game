from sys import argv
from os import listdir

STANDARD_FORMAT_OBJECT_DELIMITER = "::"
STANDARD_FORMAT_EVENT_DELIMITER = "=="
DESCRIPTION_KEYWORD = "examine"
EVENTS_KEYWORD = "events"
OBJECTS_KEYWORD = "objects"
ROOMS_KEYWORD = "rooms"

def standard_format_parser_room( room_name, text ):

    fragments = text.split( STANDARD_FORMAT_OBJECT_DELIMITER )
    room = {
        EVENTS_KEYWORD : {},
        OBJECTS_KEYWORD : {}
    }

    # first we parse objects
    for i in range( 1, len( fragments ), 2 ):

        name = fragments[ i ].strip()
        subfragments = fragments[ i + 1 ].split( STANDARD_FORMAT_EVENT_DELIMITER )
        description = subfragments[ 0 ].strip()
        events = { DESCRIPTION_KEYWORD : description }
        room[ OBJECTS_KEYWORD ][ name ] = {}

        if len( subfragments ) > 1:
            for j in range( 1, len( subfragments ), 2 ): 
                events[ subfragments[ j ].strip() ] = subfragments[ j + 1 ].strip()

        if name == room_name:
            room[ EVENTS_KEYWORD ] = events
        else:
            room[ OBJECTS_KEYWORD ][ name ][ EVENTS_KEYWORD ] = events

    return room
        

def standard_format_parser( folder ):
    rooms = []
    game = { ROOMS_KEYWORD: {} }

    for filename in listdir( folder ):
   
        parts = filename.split( "." )

        if len( parts ) > 1 and parts[ -1 ] == 'tg':
            name = ".".join( parts[ 0: - 1 ] )
            room = standard_format_parser_room( name, open( filename, 'r' ).read() )
            game[ ROOMS_KEYWORD ][ name ] = room

    return game
