const express = require('express');
const fs = require('fs').promises;
const path = require('path');
const app = express();
const PORT = 3000;

// Como o server.js está dentro de '/router', voltamos uma pasta (..) para a raiz
const DB_FILE = path.join(__dirname, '../database.json');
const HTML_FILE = path.join(__dirname, '../html.html');

app.use(express.json());
app.use((err, req, res, next) => {
    if (err instanceof SyntaxError && err.status === 400 && 'body' in err) {
        return res.status(400).json({ erro: 'Formato JSON inválido.' });
    }
    next();
});

async function lerBanco() {
    try {
        const dados = await fs.readFile(DB_FILE, 'utf8');
        return JSON.parse(dados);
    } catch (erro) {
        return { usuarios: {} };
    }
}

async function salvarBanco(dados) {
    await fs.writeFile(DB_FILE, JSON.stringify(dados, null, 4));
}

// ---------------------------------------------------------
// NOVA ROTA DO PAINEL DE CONTROLE
// ---------------------------------------------------------

// Agora o HTML só abre se acessar /config_server
app.get('/config_server', (req, res) => {
    res.sendFile(HTML_FILE);
});

// Retorna os dados para o painel montar a lista
app.get('/api/dados', async (req, res) => {
    const db = await lerBanco();
    res.json(db);
});

// ---------------------------------------------------------
// ROTAS DO CARRINHO (API RESTful)
// ---------------------------------------------------------

app.post('/api/users/:userId/carrinho/:cartId', async (req, res) => {
    const { userId, cartId } = req.params;
    const db = await lerBanco();

    if (!db.usuarios[userId]) {
        db.usuarios[userId] = { carrinhos: {} };
    }

    db.usuarios[userId].carrinhos[cartId] = {
        ultima_atualizacao: new Date().toLocaleString('pt-BR'),
        dados: req.body
    };

    await salvarBanco(db);
    console.log(`[+] Dados atualizados: Usuário ${userId} | Carrinho ${cartId}`);
    res.json({ status: 'Sucesso' });
});

app.delete('/api/users/:userId/carrinho/:cartId', async (req, res) => {
    const { userId, cartId } = req.params;
    const db = await lerBanco();

    if (db.usuarios[userId] && db.usuarios[userId].carrinhos[cartId]) {
        delete db.usuarios[userId].carrinhos[cartId];
        if (Object.keys(db.usuarios[userId].carrinhos).length === 0) {
            delete db.usuarios[userId];
        }
        await salvarBanco(db);
        console.log(`[-] Carrinho deletado: Usuário ${userId} | Carrinho ${cartId}`);
        res.json({ status: 'Sucesso' });
    } else {
        res.status(404).json({ erro: 'Não encontrado.' });
    }
});

app.listen(PORT, '0.0.0.0', () => {
    console.log(`🚀 Servidor rodando na porta ${PORT}`);
    console.log(`👉 Acesse o painel em: http://localhost:${PORT}/config_server`);
});