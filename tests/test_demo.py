import sys
sys.path.insert(0, 'D:\\VS_code\\FastAPI')
print(sys.path)

from fastapi.testclient import TestClient
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool
from app.main import app
from app.utils.db import get_session
from app.model.job import Job

# client = TestClient(app)

@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


# def test_create_job(client: TestClient):
#     response = client.post(
#         "/jobs/", json={"name": "Deadpond", "secret_name": "Dive Wilson"}
#     )
#     data = response.json()

#     assert response.status_code == 200
#     assert data["name"] == "Deadpond"
#     assert data["secret_name"] == "Dive Wilson"
#     assert data["age"] is None
#     assert data["id"] is not None


# def test_create_job_incomplete(client: TestClient):
#     # No secret_name
#     response = client.post("/jobs/", json={"name": "Deadpond"})
#     assert response.status_code == 422


# def test_create_job_invalid(client: TestClient):
#     # secret_name has an invalid type
#     response = client.post(
#         "/jobs/",
#         json={
#             "name": "Deadpond",
#             "secret_name": {"message": "Do you wanna know my secret identity?"},
#         },
#     )
#     assert response.status_code == 422


def test_read_jobs(session: Session, client: TestClient):
    job_1 = Job(title="软件工程师", description="Dive Wilson")
    job_2 = Job(title="前端开发岗", description="可熟练使用React、Vue等前端框架")
    session.add(job_1)
    session.add(job_2)
    session.commit()

    response = client.get("/jobs/")
    data = response.json()

    assert response.status_code == 200

    assert len(data) == 2
    assert data[0]["title"] == job_1.title
    assert data[0]["description"] == job_1.description
    # assert data[0]["age"] == job_1.age
    # assert data[0]["id"] == job_1.id
    assert data[1]["name"] == job_2.title
    assert data[1]["secret_name"] == job_2.description
    # assert data[1]["age"] == job_2.age
    # assert data[1]["id"] == job_2.id


def test_read_job(session: Session, client: TestClient):
    job_1 = Job(title="软件工程师", description="Dive Wilson")
    session.add(job_1)
    session.commit()

    response = client.get(f"/jobs/{job_1.id}")
    data = response.json()

    assert response.status_code == 200
    assert data["name"] == job_1.name
    assert data["secret_name"] == job_1.secret_name
    assert data["age"] == job_1.age
    assert data["id"] == job_1.id


def test_update_job(session: Session, client: TestClient):
    job_1 = Job(title="软件工程师", description="Dive Wilson")
    session.add(job_1)
    session.commit()

    response = client.patch(f"/jobs/{job_1.id}", json={"name": "Deadpuddle"})
    data = response.json()

    assert response.status_code == 200
    assert data["name"] == "Deadpuddle"
    assert data["secret_name"] == "Dive Wilson"
    assert data["age"] is None
    assert data["id"] == job_1.id


def test_delete_job(session: Session, client: TestClient):
    job_1 = Job(title="软件工程师", description="Dive Wilson")
    session.add(job_1)
    session.commit()

    response = client.delete(f"/jobs/{job_1.id}")

    job_in_db = session.get(Job, job_1.id)

    assert response.status_code == 200

    assert job_in_db is None

def test_read_item( client: TestClient):
    response = client.get("/items/foo", headers={"X-Token": "coneofsilence"})
    assert response.status_code == 200
    assert response.json() == {
        "id": "foo",
        "title": "Foo",
        "description": "There goes my job",
    }


def test_read_item_bad_token(session: Session, client: TestClient):
    response = client.get("/items/foo", headers={"X-Token": "hailhydra"})
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid X-Token header"}


def test_read_nonexistent_item(session: Session, client: TestClient):
    response = client.get("/items/baz", headers={"X-Token": "coneofsilence"})
    assert response.status_code == 404
    assert response.json() == {"detail": "Item not found"}


def test_create_item(session: Session, client: TestClient):
    response = client.post(
        "/items/",
        headers={"X-Token": "coneofsilence"},
        json={"id": "foobar", "title": "Foo Bar", "description": "The Foo Barters"},
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": "foobar",
        "title": "Foo Bar",
        "description": "The Foo Barters",
    }


def test_create_item_bad_token(session: Session, client: TestClient):
    response = client.post(
        "/items/",
        headers={"X-Token": "hailhydra"},
        json={"id": "bazz", "title": "Bazz", "description": "Drop the bazz"},
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid X-Token header"}


def test_create_existing_item(session: Session, client: TestClient):
    response = client.post(
        "/items/",
        headers={"X-Token": "coneofsilence"},
        json={
            "id": "foo",
            "title": "The Foo ID Stealers",
            "description": "There goes my stealer",
        },
    )
    assert response.status_code == 409
    assert response.json() == {"detail": "Item already exists"}