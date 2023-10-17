import asyncio

s_url = 'https://api.thegraph.com/subgraphs/name/maxltd/rafflemarketplace'

from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport

transport = AIOHTTPTransport(url=s_url)

client = Client(transport=transport, fetch_schema_from_transport=True)

query = gql(
    """
        query MyQuery {
      raffles {
        ongoingStage
        id
        stages {
          ticketPrice
          ticketsAvailable
          stageType
          ticketsSold
        }
        currentState
        title
        images
        description
        createdAt
        raffleEndTime
        raffleAddress
      }
    }
    """
)

async def get_graph_by_id(f_id):
    f_query = gql(
        '''
        query MyQuery {
              raffle(id: "''' + f_id + '''") {
            ongoingStage
            stages {
              ticketPrice
              ticketsAvailable
              stageType
              ticketsSold
            }
            currentState
            title
            images
            description
            createdAt
            raffleEndTime
            raffleAddress
            id
          }
        }
        '''
    )
    result = await client.execute_async(f_query)
    return result

# Execute the query on the transport
async def get_grahp_by_c(f_category):
    f_query = gql(
        """
        query MyQuery {
      raffles (where: {category:"""+str(f_category)+"""}){
        ongoingStage
        id
        stages {
          ticketPrice
          ticketsAvailable
          stageType
          ticketsSold
        }
        currentState
        title
        images
        description
        createdAt
        raffleEndTime
        raffleAddress
      }
    }
    """
    )
    result = await client.execute_async(f_query)
    return result
async def get_grahp():
    result = await client.execute_async(query)
    return result

# f_looper = asyncio.get_event_loop()
# print('init run')
#
# f_looper.run_until_complete(
#     asyncio.get_event_loop().create_task(get_grahp_by_c(2)))

