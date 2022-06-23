from sys import argv
from os import listdir
import re

STANDARD_FORMAT_OBJECT_DELIMITER = "::"
STANDARD_FORMAT_EVENT_DELIMITER = "=="
DESCRIPTION_KEYWORD = "examine"
EVENTS_KEYWORD = "events"
OBJECTS_KEYWORD = "objects"
ROOMS_KEYWORD = "rooms"

class Event:

    def __init__( self, text ):
        self.text = text

    def fire( self, state, game ):
        raise Exception( "FIRE NOT IMPLEMENTED FOR THIS EVENT." )


class TextEvent:

    def __init__( self, text ):
        self.text = text

    def fire( self, state, game ):
        return self.text

class PortalEvent:
    
    def __init__( self, text, nroom ):
        self.text = text
        self.nroom = nroom

    def fire( self, state, game ):
        state[ 'room' ] = game[ "rooms" ][ self.nroom ]
        return self.text


EVENT_FACTORY = {
    "portal": PortalEvent,
    "default": TextEvent
}

def interpret_event( key, description ):

    pattern = re.compile( "(\(.*\))" )
    args = pattern.search( key )
    event = None
    name = None

    if args:
        args = args.group( 0 ).strip()
        name = key[ 0 : key.find( args ) ].strip()
        args = args.replace( "(", "" ).replace( ")", "" )
    else:
        name = key.strip()

    if args:
        args = args.split( "," )
        event, args = args[ 0 ], [ description ] + args[ 1: ]
    else:
        args = [ description ]

    if event and event in EVENT_FACTORY:
        event = EVENT_FACTORY[ event ]( *args )
    else:
        event = EVENT_FACTORY[ "default" ]( *args )

    return name, event



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
        
        events = { DESCRIPTION_KEYWORD : TextEvent( description ) }
        room[ OBJECTS_KEYWORD ][ name ] = {}

        if len( subfragments ) > 1:
            for j in range( 1, len( subfragments ), 2 ):
                n, e = interpret_event( subfragments[ j ].strip(), subfragments[ j + 1 ].strip() )
                events[ n ] = e


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
