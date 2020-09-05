#include <iostream>
#include <fstream>

#include <chrono>
#include <thread>

using namespace std;

const int td[] = {0, 1, 0, -1};
const int tc[] = {1, 0, -1, 0};

int player_id, turn, N;
int board[105][105];

bool inside(int r, int c)
{
    return r > 0 && r <= N && c > 0 && c <= N;
}

int main()
{
    ifstream ifs("GAME.INP");
    ofstream ofs("GAME.OUT");

    ifs >> player_id >> turn >> N;
    string ss;
    getline(ifs,ss,'\n');
    for(int i = 1; i <= N; i++) 
    {
        string inter;
        getline(ifs, inter);
        for(int j = 0; j < (int)inter.size(); j++)
        {
            board[i][j+1] = inter[j] - '0';
        }
    }
    ifs.close();

    // for(int i = 1; i <= N; i++) for (int j = 1; j <= N; j++) cout << board[i][j] << " \n"[j==N];
    // cout << "----------------\n";

    for(int i = 1; i <= N; i++)
    {
        for(int j = 1; j <= N; j++)
        {
            if (board[i][j] == player_id)
            {
                for(int k = 0; k < 4; k++)
                {
                    int vr = i + td[k];
                    int vc = j + tc[k];
                    if (inside(vr, vc) && board[vr][vc] == 0)
                    {
                        ofs << "SET " << vr << " " << vc << "\n";
                        ofs.close();
                        return 0;
                    }
                }
            }
        }
    }

    return 0;
}