

class TestExercises:
    async def test_create_exercise(self, client, auth_headers):
        """Создание упражнения возвращает 201 и данные."""
        response = await client.post(
            "/exercises/",
            json={
                "name": "Приседания",
                "description": "Базовое упражнение",
            },
            headers=auth_headers,
        )
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Приседания"
        assert "id" in data

    async def test_create_exercise_duplicate_name(self, client, auth_headers, exercise):
        """Создание упражнения с дублирующимся именем возвращает 400."""
        response = await client.post(
            "/exercises/",
            json={
                "name": exercise["name"],
                "description": "Другое описание",
            },
            headers=auth_headers,
        )
        assert response.status_code == 400

    async def test_create_exercise_unauthorized(self, client):
        """Неавторизованный запрос возвращает 401."""
        response = await client.post(
            "/exercises/", json={"name": "Тест", "description": ""}
        )
        assert response.status_code == 401

    async def test_get_exercises_empty(self, client, auth_headers):
        """Список упражнений пуст для нового пользователя."""
        response = await client.get("/exercises/", headers=auth_headers)
        assert response.status_code == 200
        assert response.json() == []

    async def test_get_exercises(self, client, auth_headers, exercise):
        """Список содержит созданное упражнение."""
        response = await client.get("/exercises/", headers=auth_headers)
        assert response.status_code == 200
        assert len(response.json()) == 1

    async def test_get_exercise_by_id(self, client, auth_headers, exercise):
        """Получение упражнения по id."""
        response = await client.get(
            f"/exercises/{exercise['id']}", headers=auth_headers
        )
        assert response.status_code == 200
        assert response.json()["name"] == exercise["name"]

    async def test_get_exercise_not_found(self, client, auth_headers):
        """Несуществующее упражнение возвращает 404."""
        response = await client.get("/exercises/999", headers=auth_headers)
        assert response.status_code == 404

    async def test_update_exercise(self, client, auth_headers, exercise):
        """PATCH обновляет упражнение."""
        response = await client.patch(
            f"/exercises/{exercise['id']}",
            json={
                "name": "Жим лёжа широким хватом",
            },
            headers=auth_headers,
        )
        assert response.status_code == 200
        assert response.json()["name"] == "Жим лёжа широким хватом"

    async def test_update_exercise_duplicate_name(self, client, auth_headers):
        """PATCH с именем которое уже занято возвращает 400."""
        # Создаём два упражнения
        await client.post(
            "/exercises/",
            json={"name": "Упражнение А", "description": ""},
            headers=auth_headers,
        )
        ex_b = await client.post(
            "/exercises/",
            json={"name": "Упражнение Б", "description": ""},
            headers=auth_headers,
        )

        # Пытаемся переименовать Б в А
        response = await client.patch(
            f"/exercises/{ex_b.json()['id']}",
            json={
                "name": "Упражнение А",
            },
            headers=auth_headers,
        )
        assert response.status_code == 400

    async def test_update_exercise_not_found(self, client, auth_headers):
        """PATCH несуществующего упражнения возвращает 404."""
        response = await client.patch(
            "/exercises/999", json={"name": "XX"}, headers=auth_headers
        )
        assert response.status_code == 404

    async def test_delete_exercise(self, client, auth_headers, exercise):
        """Удаление упражнения возвращает 204."""
        response = await client.delete(
            f"/exercises/{exercise['id']}", headers=auth_headers
        )
        assert response.status_code == 204

        get_response = await client.get(
            f"/exercises/{exercise['id']}", headers=auth_headers
        )
        assert get_response.status_code == 404

    async def test_delete_exercise_not_found(self, client, auth_headers):
        """Удаление несуществующего упражнения возвращает 404."""
        response = await client.delete("/exercises/999", headers=auth_headers)
        assert response.status_code == 404

    async def test_other_user_cannot_see_exercise(self, client, exercise, auth_headers):
        """Другой пользователь не видит чужие упражнения."""
        await client.post(
            "/auth/register",
            json={
                "email": "other@example.com",
                "password": "otherpass",
            },
        )
        login = await client.post(
            "/auth/jwt/login",
            data={
                "username": "other@example.com",
                "password": "otherpass",
            },
        )
        other_headers = {"Authorization": f"Bearer {login.json()['access_token']}"}

        # В списке другого пользователя упражнение не видно
        response = await client.get("/exercises/", headers=other_headers)
        assert response.json() == []

        # И по id тоже не видно
        response = await client.get(
            f"/exercises/{exercise['id']}", headers=other_headers
        )
        assert response.status_code == 404
