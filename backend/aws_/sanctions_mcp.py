from sqlalchemy import create_engine, MetaData, select, func, or_
from sqlalchemy.orm import Session
from dotenv import load_dotenv
import os
from mcp.server import FastMCP

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL is None:
    raise ValueError("Must set env variable DATABASE_URL for postgres")
engine = create_engine(DATABASE_URL, echo=True)

# Autoload metadata and table
metadata = MetaData()
metadata.reflect(bind=engine)
sanctions = metadata.tables["sanctions"]


def fuzzy_search_sanctions(
    db: Session,
    first_name: str,
    last_name: str,
    max_distance: int = 2,
    limit: int = 10
):
    """
    Fuzzy search sanctions table by first and last name using Levenshtein distance.

    Args:
        db (Session): SQLAlchemy DB session.
        first_name (str): First name to search.
        last_name (str): Last name to search.
        max_distance (int): Maximum character distance.
        limit (int): Limit of results.

    Returns:
        List[Row]: Matching rows.
    """
    query = (
        select(sanctions)
        .where(
            or_(
                func.levenshtein(sanctions.c.firstName,
                                 first_name) <= max_distance,
                func.levenshtein(sanctions.c.lastName,
                                 last_name) <= max_distance
            )
        )
        .limit(limit)
    )
    result = db.execute(query)
    return [dict(row._mapping) for row in result]


mcp = FastMCP("Sanctions Server", port=8002)


@mcp.tool(description="Get top 10 sanctions results based on first_name last_name")
def search_sanctions(first_name: str, last_name: str):
    with Session(engine) as session:
        results = fuzzy_search_sanctions(
            session, first_name=first_name, last_name=last_name)
        print(results)
    return results


mcp.run(transport="streamable-http")
